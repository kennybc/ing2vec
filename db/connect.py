from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from os import getenv

load_dotenv()


class Database:
    def __init__(self):
        self.client = MongoClient(
            getenv("MONGODB_URI"), tls=True, tlsCAFile=certifi.where()
        )

    def get_client(self):
        return self.client["Crawler"]
