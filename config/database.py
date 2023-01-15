from pymongo import MongoClient
import urllib.parse
from decouple import config

mongo_pass = config("mongo_pass")
password = urllib.parse.quote_plus(mongo_pass)
client = MongoClient("mongodb+srv://kiran_nayak:%s@cluster0.qy1iewv.mongodb.net/?retryWrites=true&w=majority" % (password))
db = client.smart_parker