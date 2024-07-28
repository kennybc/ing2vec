from db.connect import Database
import numpy as np
from bson.objectid import ObjectId
import math
import json
import pymongo
import networkx as nx

db = Database().get_client()


def get_nodes():
    nodes = []
    for node in db["ingredients"].find():
        nodes.append(node)
    return nodes


def get_neighbors(node):
    node = str(node["_id"])
    neighbors = []
    for neighbor in db["edges"].find({"$or": [{"node1": node}, {"node2": node}]}):
        if neighbor["node1"] == node:
            neighbor_id = neighbor["node2"]
        else:
            neighbor_id = neighbor["node1"]

        neighbors.append(
            {
                "id": neighbor_id,
                "name": db["ingredients"].find_one({"_id": ObjectId(neighbor_id)})[
                    "name"
                ],
                "weight": neighbor["count"],
            }
        )

    return neighbors


def has_edge(node1, node2):
    return db["edges"].count_documents(
        {
            "$or": [
                {"$and": [{"node1": node1}, {"node2": node2}]},
                {"$and": [{"node1": node2}, {"node2": node1}]},
            ]
        }
    )


def generate_graph():
    graph = nx.Graph()
    ingredients = db["ingredients"].find()
    for ingredient in ingredients:
        graph.add_node(
            str(ingredient["_id"]), name=ingredient["name"], count=ingredient["count"]
        )

    least_pmi = 0
    edges = db["edges"].find()
    total_edges = db["edges"].count_documents({})
    for edge in edges:
        # cocurrency count as edge weight
        # graph.add_edge(edge["node1"], edge["node2"], weight=edge["count"])

        # PMI as edge weight
        total_nodes = len(graph.nodes)
        pxy = edge["count"] / total_edges  # p(x and y)
        px = graph.nodes[edge["node1"]]["count"] / total_nodes  # p(x)
        py = graph.nodes[edge["node2"]]["count"] / total_nodes  # p(y)
        pmi = math.log(pxy / (px * py), 2)
        graph.add_edge(edge["node1"], edge["node2"], weight=pmi)

        if pmi < least_pmi:
            least_pmi = pmi

    # add most negative PMI to all edge weights to ensure all are positive
    for _, _, edge in graph.edges(data=True):
        edge["weight"] += abs(least_pmi)

    return graph


def flatten_walks():
    walks = []
    for walk in db["walks"].find():
        walks.append(walk["walk"])

    return walks


# q biases walks to look for nodes further away;
# the lower q is, the further away it looks
# p biases the probability to return to the immediately previous node in the walk
# a lower p increases the probability to keep the walk path more local/tight
def generate_walks(walks_per_node=50, walk_length=25, p=1.0, q=1.0):
    graph = generate_graph()
    print(graph)

    def get_next_node(node, prev):
        weights = []
        neighbors = list(graph.neighbors(node))
        for neighbor in neighbors:
            if neighbor == prev:
                weights.append(graph[node][neighbor]["weight"] / p)
            elif graph.has_edge(neighbor, prev):
                weights.append(graph[node][neighbor]["weight"])
            else:
                weights.append(graph[node][neighbor]["weight"] / q)

        weight_sum = sum(weights)
        probs = [weight / weight_sum for weight in weights]
        return np.random.choice(neighbors, p=probs)

    # get last walk: walks store the origin node and index so
    # if walk generation is interrupted, it can pick up from where it left off
    last = db["walks"].find_one(sort=[("_id", pymongo.DESCENDING)])
    if last is None:
        last = {"node": "0", "walk_index": -1}

    skipped_last = False
    for id, node in graph.nodes(data=True):
        # skip nodes we've already generated walks for
        if id <= last["node"]:
            continue

        walks_remaining = walks_per_node - last["walk_index"] - 1

        if skipped_last:
            walks_remaining = walks_per_node

        walks_from_node = []
        for walk_index in range(walks_remaining):
            prev = id
            walk = [node["name"]]
            for _ in range(walk_length):
                next = get_next_node(id, prev)
                walk.append(graph.nodes[next]["name"])
                prev = next

            walk_doc = {"node": id, "walk_index": walk_index, "walk": walk}
            walks_from_node.append(walk_doc)

        if not walks_from_node:
            skipped_last = True
            continue

        db["walks"].insert_many(walks_from_node)
        """print(
            "Random walk progress: "
            + str(walk_index)
            + "/"
            + str(graph.number_of_nodes()),
            flush=True,
        )"""
