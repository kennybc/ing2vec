from db.connect import Database
import numpy as np
from bson.objectid import ObjectId
import json

db = Database().get_client()


def get_nodes():
    nodes = []
    for node in db["Ingredients"].find():
        nodes.append(node)
    return nodes


def get_neighbors(node):
    node = str(node["_id"])
    neighbors = []
    for neighbor in db["Edges"].find({"$or": [{"node1": node}, {"node2": node}]}):
        if neighbor["node1"] == node:
            neighbor_id = neighbor["node2"]
        else:
            neighbor_id = neighbor["node1"]

        neighbors.append(
            {
                "id": neighbor_id,
                "name": db["Ingredients"].find_one({"_id": ObjectId(neighbor_id)})[
                    "name"
                ],
                "weight": neighbor["count"],
            }
        )

    return neighbors


def has_edge(node1, node2):
    return db["Edges"].count_documents(
        {
            "$or": [
                {"$and": [{"node1": node1}, {"node2": node2}]},
                {"$and": [{"node1": node2}, {"node2": node1}]},
            ]
        }
    )


# q biases walks to look for nodes further away;
# the lower q is, the further away it looks
# p biases the probability to return to the immediately previous node in the walk
# a lower p increases the probability to keep the walk path more local/tight
def generate_walks(walks_per_node=10, walk_length=50, p=1.0, q=1.0):
    nodes = get_nodes()

    def get_next_node(node, prev):
        weights = []
        neighbors = get_neighbors(node)
        for neighbor in neighbors:
            if neighbor["id"] == prev["id"]:
                weights.append(neighbor["weight"] / p)
            elif has_edge(node["_id"], neighbor["id"]):
                weights.append(neighbor["weight"])
            else:
                weights.append(neighbor["weight"] / q)

        weight_sum = sum(weights)
        probs = [weight / weight_sum for weight in weights]
        return np.random.choice(neighbors, p=probs)

    walks = []

    for node in nodes:
        for _ in range(walks_per_node):
            prev = {"id": node["_id"]}
            walk = [node["name"]]
            for _ in range(walk_length):
                next = get_next_node(node, prev)
                walk.append(next["name"])
                prev = next

            walks.append(walk)
            print(
                "Random walk progress: "
                + str(len(walks))
                + "/"
                + str(len(nodes) * walks_per_node)
            )

    with open("./node2vec/data.json", "w") as f:
        json.dump(walks, f)
    print(walks)
