from urllib.parse import unquote
from db.connect import Database
from fastapi import FastAPI
from parser.train import train
from parser.infer import infer

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


@app.get("/infer/{phrase}")
async def infer_ingredients(phrase):
    phrase = unquote(phrase)
    return infer(phrase)


@app.get("/train")
def train_model():
    train()
