from gensim.models import Word2Vec
from pathlib import Path
from sklearn.manifold import TSNE
import pandas as pd
import json

here = Path(__file__).parent


def train2():
    data = []
    with open("./node2vec/data.json") as f:
        data = json.load(f)
    model = Word2Vec(
        sentences=data,
        vector_size=100,
        window=5,
        min_count=1,
        workers=4,
    )
    model.save("./node2vec/word2vec.model")


def get_words(word):
    model = Word2Vec.load("./node2vec/word2vec.model")
    vector = model.wv["chicken broth"]  # get numpy vector of a word
    sims = model.wv.most_similar("chicken broth", topn=3)  # get other similar words

    print(vector)
    print(sims)

    vocab = list(model.wv.key_to_index)
    X = model.wv[vocab]
    tsne = TSNE(n_components=2, perplexity=5)
    X_tsne = tsne.fit_transform(X)
    df = pd.DataFrame(X_tsne, index=vocab, columns=["x", "y"])
    print(df)
