from urllib.parse import unquote
from db.connect import Database
from fastapi import FastAPI
from parser.predict import predict_ingredients, predict_labels
from parser.train import train
from parser.test import test


app = FastAPI()

conn = Database()
db = conn.get_client()


@app.get("/recipe/{url}")
async def get_recipe_by_url(url):
    url = unquote(url)
    if url == "latest":
        from pymongo import DESCENDING
        latest = db.find_one({}, sort=[("_id", DESCENDING)])
    else:
        latest = db.find_one({"url": url})

    if latest is None:
        latest = {}
    else:
        del latest["_id"]

    return latest


@app.get("/parse/{phrase}")
async def parse_ingredient_phrase(phrase):
    phrase = unquote(phrase)
    return {
        "labels": predict_labels(phrase),
        "ingredients": predict_ingredients(phrase)
    }


@app.get("/train")
async def train_parser():
    train()


@app.get("/test")
async def test_parser():
    test()
