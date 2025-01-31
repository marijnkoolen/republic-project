import datetime
import os
import subprocess
from typing import Dict, List

from fuzzy_search.tokenization.string import score_levenshtein_similarity_ratio

import republic


def get_project_dir() -> str:
    module_dir = str(republic.__path__[0])
    return os.path.split(module_dir)[0]


def get_commit_version():
    # Get the Git repository commit hash for keeping provenance
    completed_process = subprocess.run(["git", "rev-parse", "HEAD"], encoding='utf-8', stdout=subprocess.PIPE)
    return completed_process.stdout.strip() if completed_process is not None else None


def get_commit_url():
    commit_version = get_commit_version()
    return f'https://github.com/HuygensING/republic-project/commit/{commit_version}'


def get_iso_utc_timestamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')


def make_index_urls(es_config, doc_ids: List[str], index: str, es_url: str = None):
    if es_url is None:
        if 'elastic_config' not in es_config:
            print(f'url in config: {"url" in es_config}')
            print(es_config['url'])
        es_url = es_config['elastic_config']['url']
    if isinstance(doc_ids, str):
        doc_ids = [doc_ids]
    return [f'{es_url}{index}/_doc/{doc_id}' for doc_id in doc_ids]


def make_provenance_data(es_config, source_ids: List[str], target_ids: List[str],
                         source_index: str, target_index: str, source_es_url: str = None,
                         source_external_urls: List[str] = None, why: str = None) -> Dict[str, any]:
    if source_es_url is None:
        source_es_url = es_config['elastic_config']['url']
    target_es_url = es_config['elastic_config']['url']
    if isinstance(source_ids, str):
        source_ids = [source_ids]
    if isinstance(target_ids, str):
        target_ids = [target_ids]
    if source_index == 'Loghi':
        source_urls = [source_id for source_id in source_ids]
    else:
        source_urls = [f'{source_es_url}{source_index}/_doc/{source_id}' for source_id in source_ids]
    if source_external_urls is not None:
        source_urls += source_external_urls
    target_urls = [f'{target_es_url}{target_index}/_doc/{target_id}' for target_id in target_ids]
    source_rels = ['primary'] * len(source_urls)
    target_rels = ['primary'] * len(target_urls)
    commit_url = get_commit_url()
    if why is None:
        why = f'REPUBLIC CAF Pipeline deriving {target_index} from {source_index}'
    return {
        'who': 'orcid:0000-0002-0301-2029',
        'where': 'https://annotation.republic-caf.diginfra.org/',
        'when': get_iso_utc_timestamp(),
        'how': commit_url,
        'why': why,
        'source': source_urls,
        'source_rel': source_rels,
        'target': target_urls,
        'target_rel': target_rels
    }


def get_name_for_disambiguation(proposed, base_config, es=None, debug=False):
    """get a name candidate from the namenindex.
    It keeps count of a time frame and tries to select the most likely candidate.
    TODO make this more sophisticated
    and the time stuff syntax is apparently not good
    """
    year = int(base_config['year'])
    low_date_limit =  year - 85  # or do we have delegates that are over 85?
    high_date_limit = year - 20  # 20 is a very safe upper limit

    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "fuzzy": {
                            "fullname": {
                                "value": proposed.lower()
                            }
                        }
                    },
                    {
                        "range": {
                            "by": {"gt": low_date_limit,
                                   "lt": high_date_limit
                                   },
                        }
                    },
                    {
                        "range": {
                            "dy": {"lt": year + 50,
                                   "gt": year
                                   },
                        }

                    }
                ],
                "should": [
                    {"match":
                         {"collection":
                              {"query": "raa",
                               "boost": 2.0
                               }
                          }
                     }
                ]
            }
        },
        "from": 0,
        "size": 1000,
        "sort": "_score"
    }

    results = es.search(index="namenindex", body=body)
    candidate = None
    if results['hits']['total'] > 0:
        names = [r['_source']['geslachtsnaam'] for r in results['hits']['hits']]
        people = [r['_source']['fullname'] for r in results['hits']['hits']]
        interjections = people = [r['_source']['intrapositie'] for r in results['hits']['hits']]
        candidate = [r for r in results['hits']['hits']]
    # think about this some more
    print('nr of candidates: {}'.format(results['hits']['total']))
    if debug is True:
        print(body)
    return candidate  # ([names, people])


def one_match(matchgrp):
    """returns one (hopefully the  best) match from a list of matches"""
    gr = {}
    for sr in matchgrp:
        if gr.get(sr[1]):
            gr[sr[1]].append(sr)
        else:
            gr[sr[1]] = [sr]
    for key in gr.keys():
        nw = min(gr[key], key=lambda x: x[2])
        gr[key] = nw
    return gr


# this is straight from the python docs
from itertools import tee


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def check_overlap(a, b, minlen=1):
    overlap = set(a) & set(b)
    if len(overlap) > minlen:
        result = True
    else:
        result = False
    return result

check_overlap(range(10, 20), range(12, 30), minlen=1)


def get_span_from_regex(r):
    m = r.group(0)
    s1 = r.string.find(m)
    s2 = s1 + len(m)
    return (s1, s2)

# merge lists from stackoverflow
# https://stackoverflow.com/questions/9110837/python-simple-list-merging-based-on-intersections


def merge(lsts):
    sets = [set(lst) for lst in lsts if lst]
    merged = True
    while merged:
        merged = False
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = True
                    common |= x
            results.append(common)
        sets = results
    return sets


def reverse_dict(d):
    """this returns a reverse mapping of a dictionary with key:[values] as single_value:key dictionary
    which is handy for storing variants in a database"""
    return {svalue: key for key, value in d.items() for svalue in value}


def levenst_vals(x, txt, threshold=0.8):
    scores= [score_levenshtein_similarity_ratio(i, txt) for i in x if len(i)>2 and score_levenshtein_similarity_ratio(i,txt) > 0.5]
    result = False
    if len(scores) > 0:
        if max(scores) > threshold:
            result = True
    return result

# def marker(text='', item=None, keywords=[], searcher=None, itemtype='', color='black'):
#     kw_searcher = searcher
#     kw_searcher.index_keywords(keywords)
#     for kw in keywords:
#         provs = kw_searcher.find_candidates_new(keyword=kw, text=text)
#     if len(provs) > 0:
#         profset = provs[0].get('match_offset') or 0
#     # mt.colormap[itemtype] = color
#     for res in provs:
#         ofset = res['match_offset']
#         span = (ofset, ofset + len(res['match_string']))
#         if span not in item.spans:
#             item.set_span(span, itemtype)

# from scipy.special import softmax
# from numpy import argmax


# get best score from a fuzzy_search. This does not account for the length of a match
def score_match(match):
    """score fuzzy_search phrase searcher matches"""
    result = sum([match.levenshtein_similarity, match.character_overlap, match.ngram_overlap, score_levenshtein_similarity_ratio(str(match.variant.exact_string),str(match.phrase.exact_string))])
    return result


def best_match(matches=[]):
    """
    calculates best match from fuzzysearch matches based on scorematch. Returns single match
    TODO: this does not account for best length if match scores are equal"""
    if matches:
        mn = min([abs(len(m.phrase.exact_string) - len(m.string)) for m in matches])
        candidates = [m for m in matches if abs(len(m.phrase.exact_string) - len( m.string)) == mn]
        mx = max([score_match(m) for m in matches])
        candidates = [m for m in matches if score_match(m) == mx]
        candidate = max([m for m in candidates if score_match(m) == mx], key=lambda x: score_match(x))
        return candidate

