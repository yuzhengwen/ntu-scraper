from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["DevDB"]
collection = db["mods"]

def insert_data(data):
    print("Inserting data")
    collection.insert_one(data)

def insert_many(data):
    print("Inserting many data")
    collection.insert_many(data)