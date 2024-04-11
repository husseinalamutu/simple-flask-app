from config import Config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# import dns.resolver

# dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers=['8.8.8.8']

# Create a new client and connect to the server
client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
db = client["injozi"]
users_collection = db["users"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)