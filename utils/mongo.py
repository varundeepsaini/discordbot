from pymongo import MongoClient, database
from .env import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.saini_certified
user_collection = db.users
problems_collection = db.problems
