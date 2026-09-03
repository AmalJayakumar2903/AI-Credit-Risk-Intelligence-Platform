import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)

db = client["credrisk_analyzer"]

analyses_collection = db["analyses"]
documents_collection = db["documents"]

def save_document(document):
    result = documents_collection.insert_one(document)

    return str(result.inserted_id)