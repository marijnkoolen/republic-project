import glob
import os
import pickle
import multiprocessing

from republic.helper.utils import get_project_dir
from republic.nlp.entities import tag_resolution
from republic.nlp.entities import load_tagger
from republic.nlp.entities import read_res_file_map
from republic.nlp.entities import read_para_res_map
from republic.nlp.entities import write_layer_annotations
from republic.nlp.entities import get_anno_files
from republic.nlp.read import read_paragraphs
from republic.nlp.tag_formulas import tag_inventory_formulas


NER_TYPES = {'HOE', 'PER', 'COM', 'ORG', 'LOC', 'DAT', 'RES'}
ENTITY_TYPES = NER_TYPES.union({'FORM'})


def read_para_files(para_dir: str):
    return sorted(glob.glob(os.path.join(para_dir, 'resolution*.tsv.gz')))


def tag_paragraph_formulas(task):
    tag_inventory_formulas(task['inv_num'], debug=0)


def tag_paragraph_entities(task):
    inv_num = task['para_file'].split('-')[-1][:4]
    assert 3 <= len(inv_num) <= 4 and inv_num.isdigit(), f"unexpected para_file name: {task['para_file']}"
    entities_file = os.path.join(task['entities_dir'],
                                 f"entity_annotations-layer_{task['layer_name']}-inv_{inv_num}.pcl")
    annotations = []
    count = 0
    for para_json in read_paragraphs(task['para_file'], as_json=True, has_header=True):
        if 'para_type' in para_json and para_json['para_type'] in {'marginalia'}:
            continue
        annos = tag_resolution(para_json['text'], para_json['para_id'], task['model'])
        annotations.extend(annos)
        count += 1
        if count % 100 == 0:
            print(f"{task['layer_name']}\tinv: {inv_num}\tresolutions: {count: >8}"
                  f"\tannotations: {len(annotations): >8}")
    print(f"{task['layer_name']}\tinv: {inv_num}\tresolutions: {count: >8}\tannotations: {len(annotations): >8}")
    with open(entities_file, 'wb') as fh:
        pickle.dump(annotations, fh)


def aggregate_entity_output(entity_dir: str, para_dir: str):
    anno_version = 'Nov-2024'
    anno_subdir = f'annotations-{anno_version}'
    annotation_dir = os.path.join(entity_dir, anno_subdir)
    para_res_map = read_para_res_map(para_dir)
    res_file_map = read_res_file_map(para_dir)
    layer_anno_files = get_anno_files(annotation_dir)

    aggregations_dir = os.path.join(entity_dir, f'aggregations-{anno_version}')
    for layer in layer_anno_files:
        write_layer_annotations(layer, layer_anno_files, para_res_map, res_file_map,
                                aggregations_dir, anno_subdir)


def print_usage():
    print(f'usage: {__name__} --layers=LAYER1:LAYER2')


def parse_args():
    argv = sys.argv[1:]
    # Define the getopt parameters
    try:
        opts, args = getopt.getopt(argv, 'l:', ['layers='])
        layers = None
        for opt, arg in opts:
            print(f"opt: {opt}\targ: {arg}")
            if opt in {'-l', '--layers'}:
                layers = arg
                if ':' in layers:
                    layers = layers.split(':')
                else:
                    layers = [layers]
                assert all([layer in ENTITY_TYPES for layer in layers])
        if layers is None:
            layers = NER_TYPES
            print('no layer specified, using all NER layers')
        print('training layers:', layers)
        return layers
    except getopt.GetoptError:
        # Print something useful
        print_usage()
        sys.exit(2)


def main():
    project_dir = get_project_dir()

    num_epochs = 15
    num_processes = 10
    layers = parse_args()

    if 'FORM' in layers and len(layers) > 1:
        raise ValueError('Cannot combine FORM tagging with other layers, as FORM uses multiprocessing and the others cannot')

    if 'FORM' in layers:
        tasks = []
        for inv_num in range(3760, 3865):
            task = {
                'inv_num': str(inv_num),
            }
            tasks.append(task)
        with multiprocessing.Pool(processes=num_processes) as pool:
            pool.map(tag_paragraph_formulas, tasks)
    else:
        entities_dir = 'data/entities/annotations-Nov-2024'
        para_dir = 'data/paragraphs/entities-Nov-2024'
        # para_dir = 'data/paragraphs/test'
        para_files = read_para_files(para_dir)
        print('num para files:', len(para_files))
        for layer_name in layers:
            model = load_tagger(layer_name=layer_name)
            for para_file in para_files:
                task = {
                    'para_file': para_file,
                    'layer_name': layer_name,
                    'model': model,
                    'entities_dir': entities_dir
                }
                tag_paragraph_entities(task)
        aggregate_entity_output(entity_dir=entities_dir, para_dir=para_dir)


if __name__ == "__main__":
    import getopt
    import sys
    main()
