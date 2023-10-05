from transformers import pipeline
from pathlib import Path
import time

here = Path(__file__).parent

classifier = pipeline("ner", model=here / "./model", aggregation_strategy="first")


def infer(phrase):
    clock = time.time()
    inference = classifier(phrase)
    print("Time elapsed: " + str(time.time() - clock))
    return inference