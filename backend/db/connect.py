from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from os import getenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(
            # getenv("MONGODB_URI"),
            "localhost",
            27017,
            serverSelectionTimeoutMS=3000,  # 3 second timeout
        )

    def get_client(self):
        return self.client["ing2vec"]
