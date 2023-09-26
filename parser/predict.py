import torch
import os
import json
import pickle
from pathlib import Path
from argparse import ArgumentParser
from parser.model import IngredientParser
from parser.preprocess import convert_number, preprocess, Vocabulary


here = Path(__file__).parent


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


def predict_labels(phrases):
    model_path = here / "./save/"
    encoder_vocab_path = here / './data/vocab.pkl'
    with open(encoder_vocab_path, 'rb') as f:
        vocab = pickle.load(f)

    with open(here / "config.json", "r") as fp:
        config = json.load(fp)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = IngredientParser(vocab.word_embeddings, config["model"]).to(device)
    model.load_state_dict(torch.load(os.path.join(model_path, 'model.pt')))

    label2id = {'DF': 0, 'NAME': 1, 'O': 2, 'QUANTITY': 3,
                'SIZE': 4, 'STATE': 5, 'TEMP': 6, 'UNIT': 7}
    id2label = {v: k for k, v in label2id.items()}

    if isinstance(phrases, str):
        phrases = [phrases]

    predictions = []
    for phrase in phrases:
        phrase = phrase.lower()
        input_ids, tag_ids, sent = parser(phrase, vocab)
        with torch.no_grad():
            model.eval()
            logits = model(input_ids.unsqueeze(0).to(device),
                           tag_ids.unsqueeze(0).to(device))
            prediction = torch.argmax(logits, dim=-1)
            predicted_labels = [(o[0], p)
                                for o, p in zip(sent, list(
                                    map(lambda x: id2label[x], prediction.squeeze(0).tolist())))]
            predictions.append(predicted_labels)
    return predictions


def predict_ingredients(phrases):
    predictions = []
    for predicted_labels in predict_labels(phrases):
        predicted_ingredient = ""
        for _, (token, label) in enumerate(predicted_labels):
            if label == "NAME":
                predicted_ingredient += token + " "
        predicted_ingredient = predicted_ingredient.rstrip()
        predictions.append(predicted_ingredient)
    return predictions


if __name__ == '__main__':
    _parser = ArgumentParser()
    _parser.add_argument("-p", "--phrases", type=str,
                         metavar='INGREDIENT PHRASE', required=True)
    args = _parser.parse_args()

    phrases = args.phrases
    predict_ingredients(phrases)
