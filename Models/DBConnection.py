from pymongo import MongoClient
from decouple import config

password = config('DB_PASS')
cluster = MongoClient(f'mongodb+srv://pulibotheroku:{password}@clusterbot.b8sfd.mongodb.net/pulibot?retryWrites=true&w=majority')
db = cluster["pulibot"]

members = db["members"]
streamers = db["streamers"]
