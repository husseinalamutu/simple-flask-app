from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from db import users_collection

class User:
    @staticmethod
    def create(username, password, role):
        hashed_password = generate_password_hash(password)
        user = {"username": username, "password": hashed_password, "role": role}
        users_collection.insert_one(user)

    @staticmethod
    def get_all():
        """Retrieves all users from the collection.

        Returns:
            A cursor object containing all user documents.
        """
        return users_collection.find()

    @staticmethod
    def find_by_username(username):
        return users_collection.find_one({"username": username})

    # @staticmethod
    # def find_by_id(user_id):
    #     return users_collection.find_one({"_id": user_id})

    @staticmethod
    def update(username, data):
        users_collection.update_one({"username": username}, {"$set": data})


