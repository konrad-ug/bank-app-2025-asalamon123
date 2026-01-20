import os
from pymongo import MongoClient
from src.account import Account

class MongoAccountsRepository:
    def __init__(self, mongo_url=None, db_name=None, collection_name=None, collection=None): 
        db_name = db_name or os.getenv("MONGO_DB", "bank_app")
        collection_name = collection_name or os.getenv("MONGO_COLLECTION", "accounts")

        client = MongoClient(mongo_url)
        db = client[db_name]
        self._collection = db[collection_name]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True
            )

    def load_all(self):

