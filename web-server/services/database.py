from datetime import datetime
from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client["social_engineering"]
collection = db["predictions"]

def save_prediction(message, prediction, probability):
    doc = {
        "message": message,
        "prediction": prediction,
        "probability": probability,
        "timestamp": datetime.now().isoformat()
    }
    collection.insert_one(doc)
