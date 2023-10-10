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

    def trim_special_chars(str):
        special_chars = ["-", "'"]
        for char in special_chars:
            str = str.replace(char + " ", char)
            str = str.replace(" " + char, char)
        str = str.replace("s'", "s' ")
        return str.strip()

    def append_if_ingredient(entity):
        nonlocal ingredients, last_tag
        if entity["entity_group"] == "name":
            if last_tag == "name":
                ingredients[-1] += entity["word"]
                ingredients[-1] = trim_special_chars(ingredients[-1])
            else:
                ingredients.append(trim_special_chars(entity["word"]))
        last_tag = entity["entity_group"]

    for entity in data:
        if isinstance(entity, list):
            for ent in entity:
                append_if_ingredient(ent)
            last_tag = ""
        else:
            append_if_ingredient(entity)

    ingredients = list(dict.fromkeys(ingredients))
    return {"ingredients": list(ingredients), "labels": data}
