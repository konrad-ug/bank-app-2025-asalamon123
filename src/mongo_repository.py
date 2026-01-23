import os
from pymongo import MongoClient
from src.account import Account

class MongoAccountsRepository:
    def __init__(self, mongo_url=None, db_name=None, collection_name=None, collection=None): 
        if collection is not None:
            self._collection = collection
        else:
            import os
            from pymongo import MongoClient

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
                {"$set": {
                    "first_name": account.first_name,
                    "last_name": account.last_name,
                    "pesel": account.pesel,
                    "promo_code": account.promo_code,
                    "balance": account.balance,
                    "history": account.history
                }},
                upsert=True
            )

    def load_all(self):
        results = self._collection.find({}, {"_id": 0})  
        accounts = [Account(**doc) for doc in results]
        return accounts