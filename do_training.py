import logging
from itertools import product

from republic.nlp.lm import train_lm
from republic.nlp.lm import make_character_dictionary
from republic.nlp.lm import make_train_test_split
from republic.nlp.ner import prep_training
from republic.nlp.ner import train
from republic.nlp.read import ParaReader, read_para_files


ENTITY_TYPES = {'HOE', 'PER', 'COM', 'ORG', 'LOC', 'DAT', 'RES'}


def train_layers(layers, train_size=1.0, mini_batch_size=32, max_epochs=10):
    logging.basicConfig(filename='training_ner.log', level=logging.DEBUG)
    bool_options = [
        'use_crf',
        'use_rnn',
        'reproject_embeddings',
        'use_context',
        'use_finetuning',
        'use_resolution',
        'use_gysbert',
        #'use_fasttext'
    ]
    for p in product([True,False],repeat=7):
        params = dict(zip(bool_options,p))
        for layer in layers:
            print(f'training layer {layer}')
            print('params:', params)
            train_entity_tagger(layer_name=layer, train_size=train_size, mini_batch_size=mini_batch_size, max_epochs=max_epochs,
                                use_crf=params['use_crf'],
                                use_rnn=params['use_rnn'],
                                use_context=params['use_context'],
                                use_gysbert=params['use_gysbert'],
                                use_resolution=params['use_resolution'],
                                use_finetuning=params['use_finetuning'],
                                reproject_embeddings=params['reproject_embeddings'])


def train_entity_tagger(layer_name: str,
                        train_size: float = 1.0,
                        hidden_size=256,
                        model_max_length=512,
                        learning_rate: float = 0.05,
                        mini_batch_size: int = 32,
                        max_epochs: int = 10,
                        use_crf: bool = False,
                        use_rnn: bool = False,
                        reproject_embeddings: bool = False,
                        use_context: bool = False,
                        use_finetuning: bool = False,
                        use_resolution: bool = False,
                        use_gysbert: bool = False,
                        use_fasttext: bool = False):
    print('use_crf:', use_crf)
    trainer = prep_training(layer_name,
                            train_size=train_size,
                            hidden_size=hidden_size,
                            use_finetuning=use_finetuning,
                            use_context=use_context,
                            use_resolution=use_resolution,
                            use_gysbert=use_gysbert,
                            use_fasttext=use_fasttext,
                            use_crf=use_crf,
                            use_rnn=use_rnn,
                            reproject_embeddings=reproject_embeddings,
                            model_max_length=model_max_length)
    train(trainer, layer_name, train_size,
          learning_rate=learning_rate,
          mini_batch_size=mini_batch_size,
          max_epochs=max_epochs)


def train_language_model(para_dir: str, corpus_dir: str, is_forward_lm: bool = True,
                         character_level: bool = True, hidden_size=256,
                         sequence_length=512, nlayers: int = 1,
                         mini_batch_size: int = 32, max_epochs: int = 10):
    logging.basicConfig(filename='training_lm.log', level=logging.DEBUG)
    para_files = read_para_files(para_dir)
    para_reader = ParaReader(para_files, ignorecase=False)
    make_train_test_split(corpus_dir, para_reader=para_reader)
    make_character_dictionary(corpus_dir)
    train_lm(corpus_dir, is_forward_lm=is_forward_lm, character_level=character_level,
             hidden_size=hidden_size, nlayers=nlayers, sequence_length=sequence_length,
             mini_batch_size=mini_batch_size, max_epochs=max_epochs)


def parse_args():
    argv = sys.argv[1:]
    # Define the getopt parameters
    try:
        opts, args = getopt.getopt(argv, 'e:l:s:r:m:t',
                                   ['epochs=', 'layers=', 'train_size=', 'learning_rate=', 'mini_batch_size=', 'type='])
        train_type = None
        layers = ['single_layer']
        train_size = 1.0
        learing_rate = 0.05
        mini_batch_size = 16
        max_epochs = 10
        for opt, arg in opts:
            if opt in {'-e', '--epochs'}:
                max_epochs = int(arg)
            if opt in {'-l', '--layers'}:
                layers = arg
                if ':' in layers:
                    layers = layers.split(':')
                else:
                    layers = [layers]
                    assert all([layer in ENTITY_TYPES for layer in layers])
            if opt in {'-s', '--train_size'}:
                train_size = float(arg)
            if opt in {'-r', '--learning_rate'}:
                learing_rate = float(arg)
            if opt in {'-m', '--mini_batch_size'}:
                mini_batch_size = int(arg)
            if opt in {'-t', '--type'}:
                train_type = arg
        return layers, train_size, learing_rate, mini_batch_size, max_epochs, train_type
    except getopt.GetoptError:
        # Print something useful
        print('usage: do_training.py --type <ner|lm>')
        raise
    sys.exit(2)


def do_train_lm():
    logging.basicConfig(filename='training_lm.log', level=logging.DEBUG)
    para_dir = 'data/paragraphs/loghi'
    corpus_dir = 'data/embeddings/flair_embeddings/corpus_loghi'

    para_files = read_para_files(para_dir)
    para_reader = ParaReader(para_files, ignorecase=False)

    make_train_test_split(corpus_dir, para_reader=para_reader)
    make_character_dictionary(corpus_dir)

    train_lm(corpus_dir, is_forward_lm=True, character_level=True,
             hidden_size=256, nlayers=1, sequence_length=512,
             mini_batch_size=32, max_epochs=10)

    train_lm(corpus_dir, is_forward_lm=False, character_level=True,
             hidden_size=256, nlayers=1, sequence_length=512,
             mini_batch_size=32, max_epochs=10)


def main():
    layers, train_size, learing_rate, mini_batch_size, max_epochs, train_type = parse_args()
    print('train_type:', train_type)
    if train_type == 'ner':
        print('layers to train:', layers)
        train_layers(layers, train_size=train_size, mini_batch_size=mini_batch_size, max_epochs=max_epochs)
    elif train_type == 'lm':
        do_train_lm()
    else:
        raise ValueError(f"invalid train_type '{train_type}', must be 'ner' or 'lm'.")


if __name__ == "__main__":
    import getopt
    import sys
    print('bla')
    main()

