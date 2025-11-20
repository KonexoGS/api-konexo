from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from app import db_connection, db_password
from typing import Dict

class Database():
    def __init__(self):
        self.client: MongoClient = MongoClient(db_connection, server_api=ServerApi(version='1', strict=True, deprecation_errors=True))
        self.database_name: str = "Konexo"

    def start_session(self):
        return self.client.start_session()

    def get_collection_data(self, collection_name:str):
        db = self._get_database()
        return db.get_collection(collection_name)

    def _get_database(self):
        return self.client.get_database(self.database_name)

    def insert(self, collection_name: str, new_data: Dict):
        if not isinstance(new_data, dict):
            raise ValueError("Os dados devem ser dicionários.")

        collection  = self.get_collection_data(collection_name)
        result = collection.insert_one(new_data)
        return str(result.inserted_id)

    def delete(self, collection_name: str, data_id: str):
        if not isinstance(data_id, str) or not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")

        if not ObjectId.is_valid(data_id):
            raise ValueError("ID inválido. Tente novamente")    

        collection = self.get_collection_data(collection_name)
        deleted_data = collection.find_one_and_delete({
            "_id": ObjectId(data_id)
        })
        return deleted_data
    
    def update(self, collection_name: str, old_data_id:str, new_data: Dict):
        if not isinstance(collection_name, str) or not isinstance(new_data, dict):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")

        if not ObjectId.is_valid(data_id):
            raise ValueError("ID inválido. Tente novamente")

        collection = self.get_collection_data(collection_name)
        new_data = collection.find_one_and_update(
            filter={"_id": ObjectId(old_data_id) }, 
            update={"$set": new_data}, 
            return_document=True)
        return new_data
    
    def find_by_id(self, collection_name: str, data_id: str):
        if not isinstance(data_id, str) or not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")
        
        if not ObjectId.is_valid(data_id):
            raise ValueError("ID inválido. Tente novamente")

        collection = self.get_collection_data(collection_name)
        result = collection.find_one({
            "_id": ObjectId(data_id)
        })
        return result
    
