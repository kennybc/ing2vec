from urllib.parse import unquote
from db.connect import Database
from fastapi import FastAPI, HTTPException

# from parser.train import train
# from parser.infer import infer
from pymongo import DESCENDING
from paginate import paginate

from node2vec.train import train2, get_words
from node2vec.preprocess import load_recipe_dataset



app = FastAPI()

offline = False
try:
    conn = Database()
    db = conn.get_client()
except:
    offline = True


######################################
# Database Endpoints
#


@app.get("/recipe/{url}")
async def get_recipe_by_url(url):
    if offline:
        return

    url = unquote(url)
    recipe = {}

    if url == "latest":
        recipe = db["recipes"].find_one({}, sort=[("_id", DESCENDING)])
    else:
        recipe = db["recipes"].find_one({"url": url})

    if recipe:
        del recipe["_id"]

    return recipe


@app.get("/nodes")
async def get_nodes(page=1):
    if offline:
        return

    page = int(page)
    # return paginate(db["Ingredients"], f"nodes", {"count": {"$gt": 1}}, page, 1000)
    return paginate(db["ingredients"], f"nodes", {}, page, 1000)


@app.get("/edges")
async def get_edges(page=1):
    if offline:
        return

    page = int(page)
    # return paginate(db["Edges"], f"edges", {"count": {"$gt": 1}}, page, 1000)
    return paginate(db["edges"], f"edges", {}, page, 1000)


@app.get("/cuisine/{cuisine}")
async def get_cuisine(cuisine, page=1):
    if offline:
        return

    page = int(page)
    return paginate(db["recipes"], f"cuisine/{cuisine}", {"cuisine": cuisine}, page)


######################################
# Parser model endpoints
#


"""@app.get("/train")
def train_model():
    train()


@app.get("/infer/{phrase}")
async def infer_ingredients(phrase):
    phrase = unquote(phrase)
    return infer(phrase)"""


######################################
# Node2Vec model endpoints
#

@app.get("/load-dataset")
def download_dataset():
    load_recipe_dataset()

@app.get("/train2")
def train_model():
    train2()


@app.get("/get-words/{word}")
def get_words_from_model(word):
    get_words(word)


@app.get("/gen-walks")
async def num_nodes():
    from node2vec.preprocess import generate_walks

    generate_walks()


@app.get("/walks")
async def get_walks(page=1):
    if offline:
        return

    page = int(page)
    return paginate(db["walks"], f"walks", {}, page, 100)
