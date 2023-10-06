import json
import numpy
from pathlib import Path

here = Path(__file__).parent


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(Encoder, self).default(obj)


def postprocess_data(data):
    data = json.loads(json.dumps(data, cls=Encoder))
    ingredients = []
    last_tag = ""
    last_word = ""

    def append_if_ingredient(entity):
        nonlocal ingredients, last_tag, last_word
        if entity["entity_group"] == "name":
            if last_tag == "name":
                if entity["word"] != "-" and last_word != "-":
                    ingredients[-1] += " "
                ingredients[-1] += entity["word"]
            else:
                ingredients.append(entity["word"].replace(" - ", "-"))
        last_tag = entity["entity_group"]
        last_word = entity["word"]

    for entity in data:
        if isinstance(entity, list):
            for ent in entity:
                append_if_ingredient(ent)
        else:
            append_if_ingredient(entity)
    
    print(ingredients)
    return {"ingredients": ingredients, "labels": data}
