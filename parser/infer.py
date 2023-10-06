from pathlib import Path
from transformers import pipeline
from parser.train import train
from parser.postprocess import postprocess_data

here = Path(__file__).parent

try:
    pipe = pipeline("ner", model=here / "./model", ignore_labels=[], aggregation_strategy="average")
except:
    train()
    pipe = pipeline("ner", model=here / "./model", ignore_labels=[], aggregation_strategy="average")


def infer(phrase):
    inference = pipe(phrase)
    return postprocess_data(inference)
