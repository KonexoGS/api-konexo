from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app import db_connection, db_password

class Database():
    def __init__(self):
        self.client: MongoClient = MongoClient(db_connection, server_api=ServerApi(version='1', strict=True, deprecation_errors=True))
        self.database_name: str = "Konexo"

    def start_session(self):
        self.client._connect()

    def get_collection_data(self, collection_name:str):
        db = self.__get_database()
        return db.get_collection(collection_name)

    def __get_database(self):
        return self.client.get_database(database_name)