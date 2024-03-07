import os

class Config:
    SECRET_KEY = 'super_secret_key'
    MONGO_URI = os.environ.get("MONGO_URI")
    JWT_SECRET_KEY = 'a_jwt_secret_key'
    
