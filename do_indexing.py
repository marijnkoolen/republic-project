from typing import Dict, Union
import multiprocessing
import os
import time
import json

from elasticsearch.exceptions import ElasticsearchException
from fuzzy_search.search.phrase_searcher import FuzzyPhraseSearcher
import pagexml.parser as pagexml_parser

from republic.helper.utils import get_commit_version

import republic.download.republic_data_downloader as downloader
import republic.elastic.republic_elasticsearch as republic_elasticsearch
import republic.extraction.extract_resolution_metadata as extract_res
from republic.helper.metadata_helper import get_per_page_type_index, map_text_page_nums
from republic.helper.metadata_helper import page_num_to_page_id
from republic.helper.model_loader import load_line_break_detector

from republic.model.inventory_mapping import get_inventories_by_year, get_inventory_by_num
from republic.model.republic_text_annotation_model import make_session_text_version
import republic.model.republic_document_model as rdm
import republic.model.resolution_phrase_model as rpm

import republic.parser.logical.pagexml_session_parser as session_parser
# import republic.parser.pagexml.republic_pagexml_parser as pagexml_parser
import republic.parser.logical.pagexml_resolution_parser as res_parser
import republic.parser.logical.index_page_parser as index_parser

import run_attendancelist


# Get the Git repository commit hash for keeping provenance
commit_version = get_commit_version()

host_type = os.environ.get('REPUBLIC_HOST_TYPE')
print('host type form environment:', host_type)
if not host_type:
    message = """REPUBLIC_HOST_TYPE is not set, assuming "external".
                To use internal, set environment variable REPUBLIC_HOST_TYPE='internal'."""
    print()
    host_type = "external"
print('host_type:', host_type)

rep_es = republic_elasticsearch.initialize_es(host_type=host_type, timeout=60)

default_ocr_type = "pagexml"
base_dir = "/data/republic/"

years = [
    1763,
    1773,
    1783,
    1793
]


def zip_exists(inv_num: int, ocr_type: str):
    out_file = downloader.get_output_filename(inv_num, ocr_type, base_dir)
    if os.path.isfile(out_file):
        return True
    else:
        return False


def has_sections(inv_num: int):
    inv_metadata = rep_es.retrieve_inventory_metadata(inv_num)
    return "sections" in inv_metadata


def index_session_resolutions(session: rdm.Session,
                              opening_searcher: FuzzyPhraseSearcher,
                              verb_searcher: FuzzyPhraseSearcher) -> None:
    for resolution in res_parser.get_session_resolutions(session, opening_searcher, verb_searcher):
        rep_es.index_resolution(resolution)


def do_downloading(inv_num: int, year: int):
    print(f"Downloading pagexml zip file for inventory {inv_num} (year {year})...")
    ocr_type = "pagexml"
    downloader.download_inventory(inv_num, ocr_type, base_dir)


def do_scan_indexing_pagexml(inv_num: int, year: int):
    print(f"Indexing pagexml scans for inventory {inv_num} (year {year})...")
    for si, scan in enumerate(rep_es.retrieve_text_repo_scans_by_inventory(inv_num)):
        try:
            print('do_scan_indexing_pagexml - indexing scan', scan.id)
            rep_es.index_scan(scan)
        except ZeroDivisionError:
            print("ZeroDivisionError for scan", scan.id)


def do_page_indexing_pagexml(inv_num: int, year: int):
    print(f"Indexing pagexml pages for inventory {inv_num} (year {year})...")
    try:
        inv_metadata = rep_es.retrieve_inventory_metadata(inv_num)
    except ValueError:
        print(f"Skipping page indexing for inventory {inv_num} (year {year}), no inventory metadata")
        return None
    page_type_index = get_per_page_type_index(inv_metadata)
    text_page_num_map = map_text_page_nums(inv_metadata)
    for si, scan in enumerate(rep_es.retrieve_inventory_scans(inv_num)):
        try:
            pages = pagexml_parser.split_pagexml_scan(scan, page_type_index)
        except BaseException:
            print(scan.id)
            raise
        for page in pages:
            if page.metadata['page_num'] in text_page_num_map:
                page_num = page.metadata['page_num']
                page.metadata['text_page_num'] = text_page_num_map[page_num]['text_page_num']
                page.metadata['skip'] = text_page_num_map[page_num]['skip']
                if text_page_num_map[page_num]['problem'] is not None:
                    page.metadata['problem'] = text_page_num_map[page_num]['problem']
            if page_type_index is None:
                page.add_type('unknown')
                page.metadata['type'] = [ptype for ptype in page.type]
            elif page.metadata['page_num'] not in page_type_index:
                page.add_type("empty_page")
                page.metadata['type'] = [ptype for ptype in page.type]
                page.metadata['skip'] = True
                # print("page without page_num:", page.id)
                # print("\tpage stats:", page.stats)
            else:
                page_types = page_type_index[page.metadata['page_num']]
                if isinstance(page_types, str):
                    page_types = [page_types]
                for page_type in page_types:
                    page.add_type(page_type)
                page.metadata['type'] = [ptype for ptype in page.type]
            print('indexing page with id', page.id)
            prov_url = rep_es.post_provenance([scan.id], [page.id], 'scans', 'pages')
            page.metadata['provenance_url'] = prov_url
            rep_es.index_page(page)
        if (si+1) % 100 == 0:
            print(si+1, "scans processed")


def do_page_type_indexing_pagexml(inv_num: int, year: int):
    print(f"Updating page types for inventory {inv_num} (year {year})...")
    inv_metadata = rep_es.retrieve_inventory_metadata(inv_num)
    pages = rep_es.retrieve_inventory_pages(inv_num)
    rep_es.add_pagexml_page_types(inv_metadata, pages)
    resolution_page_offset = 0
    for offset in inv_metadata["type_page_num_offsets"]:
        if offset["page_type"] == "resolution_page":
            resolution_page_offset = offset["page_num_offset"]
    print(inv_num, "resolution_page_offset:", resolution_page_offset)
    pages = rep_es.retrieve_inventory_resolution_pages(inv_num)
    for page in sorted(pages, key=lambda x: x["metadata"]["page_num"]):
        type_page_num = page.metadata["page_num"] - resolution_page_offset + 1
        if type_page_num <= 0:
            page.metadata["page_type"].remove("resolution_page")
        else:
            page.metadata["type_page_num"] = type_page_num
        rep_es.index_page(page)


def do_session_lines_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML sessions for inventory {inv_num} (year {year})...")
    inv_metadata = rep_es.retrieve_inventory_metadata(inv_num)
    if "period_start" not in inv_metadata:
        return None
    pages = rep_es.retrieve_inventory_resolution_pages(inv_num)
    pages.sort(key=lambda page: page.metadata['page_num'])
    pages = [page for page in pages if "skip" not in page.metadata or page.metadata["skip"] is False]
    for mi, session in enumerate(session_parser.get_sessions(pages, inv_num, inv_metadata)):
        print('session received from get_sessions:', session.id)
        source_ids = session.metadata['page_ids']
        date_string = None
        for match in session.evidence:
            if match.has_label('session_date'):
                date_string = match.string
        print('\tdate string:', date_string)
        try:
            prov_url = rep_es.post_provenance(source_ids=source_ids, target_ids=[session.id],
                                              source_index='pages', target_index='session_lines')
            session.metadata['prov_url'] = prov_url
            rep_es.index_session_with_lines(session)
        except ElasticsearchException as error:
            print(session.id)
            print(session.stats)
            print(error)
            continue


def do_session_text_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML sessions for inventory {inv_num} (year {year})...")
    for mi, session in enumerate(rep_es.retrieve_inventory_sessions_with_lines(inv_num)):
        print('indexing session text for session', session.id)
        resolutions = rep_es.retrieve_resolutions_by_session_id(session.id)
        # for res in resolutions:
        #     print(res.id, res.metadata['type'])
        session_text_doc = make_session_text_version(session, resolutions)
        rep_es.index_session_with_text(session_text_doc)


def do_resolution_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML resolutions for inventory {inv_num} (year {year})...")
    opening_searcher, verb_searcher = res_parser.configure_resolution_searchers()
    has_error = False
    line_break_detector = load_line_break_detector()
    errors = []
    for session in rep_es.retrieve_inventory_sessions_with_lines(inv_num):
        print(session.id)
        if "index_timestamp" not in session.metadata:
            rep_es.es_anno.delete(index="session_lines", id=session.id)
            print("DELETING SESSION WITH ID", session.id)
            continue
        try:
            for resolution in res_parser.get_session_resolutions(session, opening_searcher,
                                                                 verb_searcher,
                                                                 line_break_detector=line_break_detector):
                prov_url = rep_es.post_provenance(source_ids=[session.id], target_ids=[resolution.id],
                                                  source_index='session_lines', target_index='resolutions')
                resolution.metadata['prov_url'] = prov_url
                rep_es.index_resolution(resolution)
        except (TypeError, KeyError) as err:
            errors.append(err)
            # pass
            raise
    print(f"finished indexing resolutions of inventory {inv_num} with {'an error' if has_error else 'no errors'}")
    for err in errors:
        print(err)


def do_resolution_phrase_match_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML resolution phrase matches for inventory {inv_num} (year {year})...")
    searcher = res_parser.make_resolution_phrase_model_searcher()
    for resolution in rep_es.scroll_inventory_resolutions(inv_num):
        print('indexing phrase matches for resolution', resolution.metadata['id'])
        num_paras = len(resolution.paragraphs)
        num_matches = 0
        for paragraph in resolution.paragraphs:
            doc = {'id': paragraph.metadata['id'], 'text': paragraph.text}
            for match in searcher.find_matches(doc):
                rep_es.index_resolution_phrase_match(match, resolution)
                num_matches += 1
                rep_es.index_resolution_phrase_match(match, resolution)
        print(f'\tparagraphs: {num_paras}\tnum matches: {num_matches}')


def do_resolution_metadata_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML resolution metadata for inventory {inv_num} (year {year})...")
    searcher = res_parser.make_resolution_phrase_model_searcher()
    relative_path = rpm.__file__.split("republic-project/")[-1]
    repo_url = 'https://github.com/HuygensING/republic-project'
    phrase_file = f'{repo_url}/blob/{get_commit_version()}/{relative_path}'
    prop_searchers = extract_res.generate_proposition_searchers()
    for resolution in rep_es.scroll_inventory_resolutions(inv_num):
        phrase_matches = extract_res.extract_paragraph_phrase_matches(resolution.paragraphs[0],
                                                                      [searcher])
        new_resolution = extract_res.add_resolution_metadata(resolution, phrase_matches,
                                                             prop_searchers['template'],
                                                             prop_searchers['variable'])
        prov_url = rep_es.post_provenance(source_ids=[resolution.id], target_ids=[resolution.id],
                                          source_index='resolutions', target_index='resolutions',
                                          source_external_urls=[phrase_file],
                                          why='Enriching resolution with metadata derived from resolution phrases')
        if 'prov_url' not in new_resolution.metadata:
            new_resolution.metadata['prov_url'] = [prov_url]
        if isinstance(new_resolution.metadata['prov_url'], str):
            new_resolution.metadata['prov_url'] = [new_resolution.metadata['prov_url']]
        if prov_url not in new_resolution.metadata['prov_url']:
            new_resolution.metadata['prov_url'].append(prov_url)
        print('\tadding resolution metadata for resolution', new_resolution.id)
        rep_es.index_resolution(new_resolution)


def do_resolution_metadata_indexing_old(inv_num: int, year: int):
    print(f"Indexing PageXML resolution metadata for inventory {inv_num} (year {year})...")
    prop_searchers = extract_res.generate_proposition_searchers()
    # proposition_searcher, template_searcher, variable_matcher = generate_proposition_searchers()
    skip_formulas = {
        'heeft aan haar Hoog Mog. voorgedragen',
        'heeft ter Vergadering gecommuniceert ',
        # 'ZYnde ter Vergaderinge geëxhibeert vier Pasporten van',
        # 'hebben ter Vergaderinge ingebraght',
        # 'hebben ter Vergaderinge voorgedragen'
    }
    attendance = 0
    no_new = 0
    for ri, resolution in enumerate(rep_es.scroll_inventory_resolutions(inv_num)):
        if resolution.metadata['type'] == 'attendance_list':
            attendance += 1
            continue
        if len(resolution.evidence) == 0:
            print('resolution without evidence:', resolution.metadata)
        if resolution.evidence[0].phrase.phrase_string in skip_formulas:
            print('skip formula:', resolution.id)
            # print(resolution.paragraphs[0].text)
            # print(resolution.evidence[0])
            # print()
            # continue
        phrase_matches = extract_res.get_paragraph_phrase_matches(rep_es, resolution)
        new_resolution = extract_res.add_resolution_metadata(resolution, phrase_matches,
                                                             prop_searchers['template'],
                                                             prop_searchers['variable'])
        if not new_resolution:
            no_new += 1
            continue
        # print(new_resolution.metadata)
        if (ri+1) % 100 == 0:
            print(ri+1, 'resolutions parsed\t', attendance, 'attendance lists\t', no_new, 'non-metadata')
        try:
            rep_es.index_resolution_metadata(new_resolution)
            rep_es.index_resolution(new_resolution)
        except:
            print('issue with resolution metadata:\n', json.dumps(new_resolution.metadata, indent=4))
            raise


def do_inventory_attendance_list_indexing(inv_num: int, year: int):
    print(f"Indexing attendance lists with spans for inventory {inv_num} (year {year})...")
    att_spans_year = run_attendancelist.run(rep_es.es_anno, year, outdir=None,
                                            verbose=True, tofile=False,
                                            source_index=rep_es.config['resolutions_index'])
    if att_spans_year is None:
        return None
    for span_list in att_spans_year:
        # print(span_list['metadata']['zittingsdag_id'])
        att_id = f'{span_list["metadata"]["zittingsdag_id"]}-attendance_list'
        att_list = rep_es.retrieve_attendance_list_by_id(att_id)
        att_list.attendance_spans = span_list["spans"]
        rep_es.index_attendance_list(att_list)


def do_inventory_lemma_reference_indexing(inv_num: int, year: int) -> None:
    print(f"Indexing lemma references for inventory {inv_num} year {year})...")
    inv_metadata = rep_es.retrieve_inventory_metadata(inv_num)
    text_page_num_map = map_text_page_nums(inv_metadata)
    page_num_map = {}
    for page_num in text_page_num_map:
        page_info = text_page_num_map[page_num]
        if "text_page_num" not in page_info or page_info["text_page_num"] is None:
            continue
        page_num_map[page_info["text_page_num"]] = page_num_to_page_id(page_num, inv_num)
    pages = rep_es.retrieve_index_pages(inv_num)
    entries = index_parser.parse_inventory_index_pages(pages)
    start_time = time.time()
    ei = 0
    for ei, entry in enumerate(entries):
        reference = index_parser.parse_reference(entry, page_num_map)
        rep_es.index_lemma_reference(reference)
        if (ei+1) % 100 == 0:
            print(f'{ei+1} or {len(entries)} lemma references indexed, in {time.time() - start_time: .2f} seconds')
    print(f'{ei+1} or {len(entries)} lemma references indexed, in {time.time() - start_time: .2f} seconds')


def process_inventory(task: Dict[str, Union[str, int]]):
    if task["type"] == "download":
        do_downloading(task["inv_num"], task["year"])
    elif task["type"] == "scans_pages":
        do_scan_indexing_pagexml(task["inv_num"], task["year"])
        do_page_indexing_pagexml(task["inv_num"], task["year"])
    elif task["type"] == "scans":
        do_scan_indexing_pagexml(task["inv_num"], task["year"])
    elif task["type"] == "pages":
        do_page_indexing_pagexml(task["inv_num"], task["year"])
    elif task["type"] == "page_types":
        do_page_type_indexing_pagexml(task["inv_num"], task["year"])
    elif task["type"] == "session_lines":
        do_session_lines_indexing(task["inv_num"], task["year"])
    elif task["type"] == "session_text":
        do_session_text_indexing(task["inv_num"], task["year"])
    elif task["type"] == "resolutions":
        do_resolution_indexing(task["inv_num"], task["year"])
    elif task["type"] == "full_resolutions":
        rep_es.config['resolutions_index'] = 'full_resolutions'
        do_resolution_indexing(task["inv_num"], task["year"])
        do_resolution_metadata_indexing(task["inv_num"], task["year"])
        do_inventory_attendance_list_indexing(task["inv_num"], task["year"])
    elif task["type"] == "phrase_matches":
        do_resolution_phrase_match_indexing(task["inv_num"], task["year"])
    elif task["type"] == "resolution_metadata":
        do_resolution_metadata_indexing(task["inv_num"], task["year"])
    elif task["type"] == "attendance_list_spans":
        do_inventory_attendance_list_indexing(task["inv_num"], task["year"])
    elif task["type"] == "lemma_references":
        do_inventory_lemma_reference_indexing(task["inv_num"], task["year"])
    else:
        raise ValueError(f'Unknown task type {task["type"]}')
    print(f"Finished indexing {task['type']} for inventory {task['inv_num']}, year {task['year']}")


def main():
    # Get the arguments from the command-line except the filename
    argv = sys.argv[1:]
    try:
        # Define the getopt parameters
        opts, args = getopt.getopt(argv, 's:e:i:n:l:', ['foperand', 'soperand'])
        start, end, indexing_step, num_processes, index_label = None, None, None, None, None
        for opt, arg in opts:
            if opt == '-n':
                num_processes = int(arg)
            if opt == '-s':
                start = int(arg)
            if opt == '-e':
                end = int(arg)
            if opt == '-i':
                indexing_step = arg
            if opt == '-l':
                index_label = arg
        if not start or not end or not indexing_step or not num_processes:
            print('usage: add.py -s <start_year> -e <end_year> -i <indexing_step> -n <num_processes> -l <label_index_name>')
            sys.exit(2)
        if index_label:
            for key in rep_es.config:
                if key.startswith(indexing_step) and key.endswith("_index"):
                    rep_es.config[key] = f"{rep_es.config[key]}_{index_label}"
                    print(key, rep_es.config[key])
        if start in range(1576, 1797):

            tasks = []
            years = [year for year in range(start, end+1)]
            for year in years:
                for inv_map in get_inventories_by_year(year):
                    task = {
                        'year': year,
                        'type': indexing_step,
                        'commit': commit_version,
                        'inv_num': inv_map['inventory_num']
                    }
                    tasks.append(task)
            print(f'indexing {indexing_step} for years', years)
        elif start in range(3000, 5000):
            inv_nums = [inv_num for inv_num in range(start, end+1)]
            tasks = [{"inv_num": inv_num, "type": indexing_step, "commit": commit_version} for inv_num in range(start, end+1)]
            for task in tasks:
                inv_map = get_inventory_by_num(task["inv_num"])
                if inv_map is None:
                    print('No inventory metadata for inventory number', task['inv_num'])
                    continue
                task["year"] = inv_map["year"]
            tasks = [task for task in tasks if 'year' in task and task['year'] is not None]
            print(f'indexing {indexing_step} for inventories', inv_nums)
        else:
            raise ValueError("Unknown start number, expecting 1576-1796 or 3760-3864")
    except getopt.GetoptError:
        # Print something useful
        print('usage: add.py -s <start_year> -e <end_year> -i <indexing_step> -n <num_processes')
        sys.exit(2)
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_inventory, tasks)


if __name__ == "__main__":
    import getopt
    import sys
    main()

