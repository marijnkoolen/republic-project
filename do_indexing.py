import os

from fuzzy_search.fuzzy_phrase_searcher import FuzzyPhraseSearcher


from republic.config.republic_config import base_config, set_config_inventory_num
import republic.download.republic_data_downloader as downloader
import republic.elastic.republic_elasticsearch as republic_elasticsearch
import republic.extraction.extract_resolution_metadata as extract_res
from republic.helper.metadata_helper import get_per_page_type_index, map_text_page_nums

from republic.model.inventory_mapping import get_inventories_by_year
from republic.model.republic_text_annotation_model import make_session_text_version
import republic.model.republic_document_model as rdm

import republic.parser.logical.pagexml_session_parser as session_parser
import republic.parser.pagexml.republic_pagexml_parser as pagexml_parser
import republic.parser.logical.pagexml_resolution_parser as resolution_parser

import run_attendancelist


host_type = os.environ.get('REPUBLIC_HOST_TYPE')
print('host type form environment:', host_type)
if not host_type:
    message = """REPUBLIC_HOST_TYPE is not set, assuming "external".
                To use internal, set environment variable REPUBLIC_HOST_TYPE='internal'."""
    print()
    host_type = "external"
print('host_type:', host_type)

es_anno = republic_elasticsearch.initialize_es_anno(host_type=host_type)
es_tr = republic_elasticsearch.initialize_es_text_repo()

rep_es = republic_elasticsearch.RepublicElasticsearch(es_anno, es_tr, base_config)

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
    for resolution in resolution_parser.get_session_resolutions(session, opening_searcher, verb_searcher):
        rep_es.index_resolution(resolution)


def do_downloading(inv_num: int, ocr_type: str, year: int):
    print(f"Downloading pagexml zip file for inventory {inv_num} (year {year})...")
    downloader.download_inventory(inv_num, ocr_type, base_dir)


def do_scan_indexing_pagexml(inv_num: int, year: int):
    print(f"Indexing pagexml scans for inventory {inv_num} (year {year})...")
    for si, scan in enumerate(rep_es.retrieve_text_repo_scans_by_inventory(inv_num)):
        rep_es.index_scan(scan)


def do_page_indexing_pagexml(inv_num: int, year: int):
    print(f"Indexing pagexml pages for inventory {inv_num} (year {year})...")
    inv_metadata = rep_es.retrieve_inventory_metadata(inv_num)
    page_type_index = get_per_page_type_index(inv_metadata)
    text_page_num_map = map_text_page_nums(inv_metadata)
    for si, scan in enumerate(rep_es.retrieve_inventory_scans(inv_num)):
        pages = pagexml_parser.split_pagexml_scan(scan)
        for page in pages:
            if page.metadata['page_num'] in text_page_num_map:
                page_num = page.metadata['page_num']
                page.metadata['text_page_num'] = text_page_num_map[page_num]['text_page_num']
                page.metadata['skip_page'] = text_page_num_map[page_num]['skip_page']
                if text_page_num_map[page_num]['problem'] is not None:
                    page.metadata['problem'] = text_page_num_map[page_num]['problem']
            if page.metadata['page_num'] not in page_type_index:
                page.add_type("empty_page")
                page.metadata['type'] = [ptype for ptype in page.type]
                page.metadata['skip_page'] = True
                print("page without page_num:", page.id)
                print("\tpage stats:", page.stats)
            else:
                page_types = page_type_index[page.metadata['page_num']]
                if isinstance(page_types, str):
                    page_types = [page_types]
                for page_type in page_types:
                    page.add_type(page_type)
                page.metadata['type'] = [ptype for ptype in page.type]
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
    pages = rep_es.retrieve_inventory_resolution_pages(inv_num)
    pages.sort(key=lambda page: page.metadata['page_num'])
    pages = [page for page in pages if "skip_page" not in page.metadata or page.metadata["skip_page"] is False]
    for mi, session in enumerate(session_parser.get_sessions(pages, inv_num, inv_metadata)):
        print('session received from get_sessions:', session.id)
        date_string = None
        for match in session.evidence:
            if match.has_label('session_date'):
                date_string = match.string
        print('\tdate string:', date_string)
        rep_es.index_session_with_lines(session)


def do_session_text_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML sessions for inventory {inv_num} (year {year})...")
    for mi, session in enumerate(rep_es.retrieve_inventory_sessions_with_lines(inv_num)):
        resolutions = rep_es.retrieve_resolutions_by_session_id(session.id)
        session_text_doc = make_session_text_version(session, resolutions)
        rep_es.index_session_with_text(session_text_doc)


def do_resolution_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML resolutions for inventory {inv_num} (year {year})...")
    opening_searcher, verb_searcher = resolution_parser.configure_resolution_searchers()
    for session in rep_es.retrieve_inventory_sessions_with_lines(inv_num):
        print(session.id)
        for resolution in resolution_parser.get_session_resolutions(session, opening_searcher,
                                                                    verb_searcher):
            rep_es.index_resolution(resolution)


def do_resolution_phrase_match_indexing(inv_num: int, year: int):
    print(f"Indexing PageXML resolution phrase matches for inventory {inv_num} (year {year})...")
    searcher = resolution_parser.make_resolution_phrase_model_searcher()
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
    print(f"Indexing PageXML resolution phrase matches for inventory {inv_num} (year {year})...")
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
            print(resolution.id)
            print(resolution.paragraphs[0].text)
            print(resolution.evidence[0])
            print()
            # continue
        phrase_matches = extract_res.get_paragraph_phrase_matches(rep_es, resolution)
        new_resolution = extract_res.add_resolution_metadata(resolution, phrase_matches,
                                                             prop_searchers['template'],
                                                             prop_searchers['variable'])
        if 'proposition_type' not in new_resolution.metadata or new_resolution.metadata['proposition_type'] is None:
            new_resolution.metadata['proposition_type'] = 'unknown'
        if not new_resolution:
            no_new += 1
            continue
        # print(new_resolution.metadata)
        if (ri+1) % 10 == 0:
            print(ri+1, 'resolutions parsed\t', attendance, 'attendance lists\t', no_new, 'non-metadata')
        rep_es.index_resolution_metadata(new_resolution)


def do_inventory_attendance_list_indexing(inv_num: int, year: int):
    print(f"Indexing attendance lists with spans for inventory {inv_num} (year {year})...")
    att_spans_year = run_attendancelist.run(rep_es.es_anno, year, outdir=None, verbose=True, tofile=False)
    for span_list in att_spans_year:
        att_id = f'{span_list["metadata"]["zittingsdag_id"]}-attendance_list'
        att_list = rep_es.retrieve_attendance_list_by_id(att_id)
        att_list.attendance_spans = span_list["spans"]
        rep_es.index_attendance_list(att_list)


def process_inventory_pagexml(inv_num, inv_config, indexing_type):
    year = inv_config["year"]
    if indexing_type == "download":
        do_downloading(inv_num, inv_config, year)
    if indexing_type == "scans_pages":
        do_scan_indexing_pagexml(inv_num, year)
        do_page_indexing_pagexml(inv_num, year)
    if indexing_type == "scans":
        do_scan_indexing_pagexml(inv_num, year)
    if indexing_type == "pages":
        do_page_indexing_pagexml(inv_num, year)
    if indexing_type == "page_types":
        do_page_type_indexing_pagexml(inv_num, year)
    if indexing_type == "session_lines":
        do_session_lines_indexing(inv_num, year)
    if indexing_type == "session_text":
        do_session_text_indexing(inv_num, year)
    if indexing_type == "resolutions":
        do_resolution_indexing(inv_num, year)
    if indexing_type == "phrase_matches":
        do_resolution_phrase_match_indexing(inv_num, year)
    if indexing_type == "resolution_metadata":
        do_resolution_metadata_indexing(inv_num, year)
    if indexing_type == "attendance_list_spans":
        do_inventory_attendance_list_indexing(inv_num, year)


def process_inventories(inv_years, ocr_type, indexing_type):
    for inv_map in get_inventories_by_year(inv_years):
        inv_num = inv_map["inventory_num"]
        inv_config = set_config_inventory_num(inv_num, ocr_type, base_config, base_dir=base_dir)
        if ocr_type == "hocr":
            # process_inventory_hocr(inv_num, inv_config, indexing_type)
            pass
        elif ocr_type == "pagexml":
            process_inventory_pagexml(inv_num, inv_config, indexing_type)


if __name__ == "__main__":
    import getopt
    import sys

    # Get the arguments from the command-line except the filename
    argv = sys.argv[1:]
    try:
        # Define the getopt parameters
        opts, args = getopt.getopt(argv, 's:e:i:', ['foperand', 'soperand'])
        start, end, indexing_step = None, None, None
        for opt, arg in opts:
            if opt == '-s':
                start = int(arg)
            if opt == '-e':
                end = int(arg)
            if opt == '-i':
                indexing_step = arg
        if not start or not end or not indexing_step:
            print('usage: add.py -s <start_year> -e <end_year> -i <indexing_step>')
            sys.exit(2)
        years = [year for year in range(start, end+1)]

    except getopt.GetoptError:
        # Print something useful
        print('usage: add.py -s <start_year> -e <end_year> -i <indexing_step>')
        sys.exit(2)
    print(f'indexing {indexing_step} for years', years)
    process_inventories(years, default_ocr_type, indexing_step)
