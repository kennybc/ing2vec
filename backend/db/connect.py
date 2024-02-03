from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from os import getenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(
            host=[getenv("MONGODB_URI")],
            serverSelectionTimeoutMS=3000,  # 3 second timeout
            username="admin",
            password="1234",
        )

    def get_client(self):
        return self.client["Crawler"]
