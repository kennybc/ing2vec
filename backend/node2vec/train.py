from gensim.models import Word2Vec
from pathlib import Path
from sklearn.manifold import TSNE
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

plt.switch_backend("agg")

from node2vec.preprocess import flatten_walks

here = Path(__file__).parent


def train2():
    data = flatten_walks()

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
    sims = model.wv.most_similar(word, topn=50)  # get other similar words

    print(sims)

    vocab = list(model.wv.key_to_index)
    X = model.wv[vocab]
    tsne = TSNE(n_components=2, perplexity=5)
    X_tsne = tsne.fit_transform(X)
    df = pd.DataFrame(X_tsne, index=vocab, columns=["x", "y"])
    df.to_csv("data.csv")
    # df.to_json("data.json", orient="records", lines=True)
