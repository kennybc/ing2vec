import torch
import os
import json
import pickle
import time
from argparse import ArgumentParser
from parser.model import IngredientParser
from parser.preprocess import convert_number, preprocess, Vocabulary


def parser(ingredient, vocab):
    tag2ids = {'RBS': 0, 'CD': 1, 'SYM': 2, 'DT': 3, '$': 4, "''": 5, 'TO': 6, 'PDT': 7, 'WP': 8, 'RBR': 9, 'POS': 10,
               'VBD': 11, 'PRP$': 12, 'IN': 13, 'VBN': 14, 'VBP': 15, 'FW': 16, 'JJR': 17, 'NNP': 18, 'JJS': 19,
               'VBZ': 20, 'RP': 21, 'WRB': 22, 'LS': 23, 'RB': 24, '.': 25, 'NN': 26, 'PRP': 27, 'JJ': 28, 'VB': 29,
               'CC': 30, 'MD': 31, ',': 32, '``': 33, 'WDT': 34, 'VBG': 35, ':': 36, 'NNS': 37, 'NNPS': 38}
    ingredient = convert_number(ingredient)
    input_ids = torch.tensor(vocab(ingredient))
    sent = preprocess(ingredient)
    assert len(sent) == len(input_ids)
    tag_ids = torch.tensor(list(map(lambda x: tag2ids.get(x[1], 0), sent)))
    return input_ids, tag_ids, sent

def parse(phrase):
    model_path = "./parser/model/"
    encoder_vocab_path = './parser/data/vocab.pkl'
    with open(encoder_vocab_path, 'rb') as f:
        vocab = pickle.load(f)

    with open(os.path.join(model_path, 'config.json'), "r") as fp:
        config = json.load(fp)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = IngredientParser(vocab.word_embeddings, config["model"]).to(device)
    model.load_state_dict(torch.load(os.path.join(model_path, 'model.pt')))

    label2id = {'DF': 0, 'NAME': 1, 'O': 2, 'QUANTITY': 3,
                'SIZE': 4, 'STATE': 5, 'TEMP': 6, 'UNIT': 7}
    id2label = {v: k for k, v in label2id.items()}

    start = time.time()
    input_ids, tag_ids, sent = parser(phrase, vocab)
    with torch.no_grad():
        model.eval()
        logits = model(input_ids.unsqueeze(0).to(device),
                       tag_ids.unsqueeze(0).to(device))
        prediction = torch.argmax(logits, dim=-1)
        predicted_labels = [(o[0], p)
                            for o, p in zip(sent, list(
                                map(lambda x: id2label[x], prediction.squeeze(0).tolist())))]
        print("- phrase:                    " + phrase)
        print("- predicted labels:          " + str(predicted_labels))
        predicted_ingredient = ""
        for i, (token, label) in enumerate(predicted_labels):
            if label == "NAME":
                predicted_ingredient += token + " "
        print("- predicted ingredient:      " + predicted_ingredient)
    end = time.time()
    print('Infer time: {}s'.format((end - start)))

if __name__ == '__main__':
    _parser = ArgumentParser()
    _parser.add_argument("-p", "--phrase", type=str,
                         metavar='INGREDIENT PHRASE', required=True)
    args = _parser.parse_args()

    phrase = args.phrase
    parse(phrase)
