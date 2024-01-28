from urllib.parse import unquote
from db.connect import Database
from fastapi import FastAPI, HTTPException
from parser.train import train
from parser.infer import infer
from pymongo import DESCENDING
from backend.paginate import paginate
from node2vec.train import train2
from node2vec.train import get_words

app = FastAPI()

offline = False
try:
    conn = Database()
    db = conn.get_client()
except:
    offline = True


@app.get("/recipe/{url}")
async def get_recipe_by_url(url):
    if offline:
        return

    url = unquote(url)
    recipe = {}

    if url == "latest":
        recipe = db["Recipes"].find_one({}, sort=[("_id", DESCENDING)])
    else:
        recipe = db["Recipes"].find_one({"url": url})

    if recipe:
        del recipe["_id"]

    return recipe


@app.get("/infer/{phrase}")
async def infer_ingredients(phrase):
    phrase = unquote(phrase)
    return infer(phrase)


@app.get("/cuisine/{cuisine}")
async def get_cuisine(cuisine, page=1):
    if offline:
        return

    page = int(page)
    return paginate(db["Recipes"], f"cuisine/{cuisine}", {"cuisine": cuisine}, page)


# @app.get("/train")
# def train_model():
#    train()


@app.get("/train2")
def train_model():
    train2()


@app.get("/get-words")
def get_words_from_model():
    get_words("cook")


@app.get("/nodes")
async def get_nodes(page=1):
    if offline:
        return

    page = int(page)
    # return paginate(db["Ingredients"], f"nodes", {"count": {"$gt": 1}}, page, 1000)
    return paginate(db["Ingredients"], f"nodes", {}, page, 1000)


@app.get("/edges")
async def get_edges(page=1):
    if offline:
        return

    page = int(page)
    # return paginate(db["Edges"], f"edges", {"count": {"$gt": 1}}, page, 1000)
    return paginate(db["Edges"], f"edges", {}, page, 1000)


@app.get("/num-nodes")
async def num_nodes():
    from node2vec.preprocess import generate_walks

    generate_walks()
