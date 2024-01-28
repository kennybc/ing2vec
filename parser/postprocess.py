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

    def trim_special_chars(str):
        special_chars = ["-", "'"]
        for char in special_chars:
            str = str.replace(char + " ", char)
            str = str.replace(" " + char, char)
        str = str.replace("s'", "s' ")
        return str.strip()

    def aggregate_names(group):
        nonlocal ingredients
        conjunctions = [",", "and", "+", "also", "plus", ";"]
        ingredient = ""
        for entity in group:
            if entity["word"] in conjunctions:
                if trim_special_chars(ingredient):
                    ingredients.append(trim_special_chars(ingredient))
                ingredient = ""
            if entity["entity_group"] == "name":
                ingredient += " " + entity["word"]

        if trim_special_chars(ingredient):
            ingredients.append(trim_special_chars(ingredient))

    if isinstance(data[0], list):
        for group in data:
            aggregate_names(group)
    else:
        aggregate_names(data)

    ingredients = list(dict.fromkeys(ingredients))
    return {"ingredients": list(ingredients), "labels": data}
