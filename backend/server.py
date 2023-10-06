from urllib.parse import unquote
from db.connect import Database
from fastapi import FastAPI
from parser.train import train
from parser.infer import infer

app = FastAPI()

conn = Database()
db = conn.get_client()

@app.get("/recipe/{url:path}")
async def get_recipe_by_url(url):
    url = unquote(url)
    recipe = {}
    if url == "latest":
        from pymongo import DESCENDING
        recipe = db.find_one({}, sort=[("_id", DESCENDING)])
    else:
        recipe = db.find_one({"url": url})

    if recipe:
        del recipe["_id"]
    
    return recipe


@app.get("/infer/{phrase}")
async def infer_ingredients(phrase):
    phrase = unquote(phrase)
    return infer(phrase)


@app.get("/train")
def train_model():
    train()
