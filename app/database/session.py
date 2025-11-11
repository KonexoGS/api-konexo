from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app import db_connection, db_password

def startSession():
    client = MongoClient(db_connection, server_api=ServerApi('1'))
    return client
