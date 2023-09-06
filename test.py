from db.connect import Database

if __name__ == '__main__':
    db = Database().get_client()
    db["Recipes"].insert_one({"name": "test"})
