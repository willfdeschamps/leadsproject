from config import MONGO_URI
import pymongo

client = pymongo.MongoClient(MONGO_URI)
mongo_db = client.test