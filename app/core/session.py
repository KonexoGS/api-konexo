from pymongo import MongoClient, ReturnDocument
from pymongo.server_api import ServerApi
from bson import ObjectId
from app import db_connection, db_password
from typing import Dict, Any

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

    def hard_delete(self, collection_name: str, data_id: str | ObjectId):
        """
        Método para a exclusão permanente do documento do banco de dados Mongo DB
        Recomendado apenas em casos especificos.

        Args:
            collection_name (str): Nome da coleção no banco de dados
            data_id Optional[str, ObjectId]: ID do conteúdo em que será excluído
        
        Returns:
            Dict: Dicionário de todo o conteúdo em que foi removido no banco.
        """


        if not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")    
        data_id = self.validate_object_id(data_id)

        collection = self.get_collection_data(collection_name)
        deleted_data = collection.find_one_and_delete({
            "_id": data_id
        })
        return deleted_data

    def delete(self, collection_name: str, data_id: str | ObjectId):
        """
        Método para a exclusão simples do siste, o conteúdo ainda existe no banco para futuros registros,
        porém não é mais encontrado pelo usuário

        Args:
            collection_name (str): Nome da coleção no banco de dados
            data_id Optional[str, ObjectId]: ID do conteúdo em que será excluído
        
        Returns:
            Dict: Dicionário de todo o conteúdo em que foi ocultado no banco.
        """

        if not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")    
        data_id = self.validate_object_id(data_id)

        collection = self.get_collection_data(collection_name)
        deleted_data = collection.find_one_and_update(
            filter={"_id": data_id,
                    "is_deleted": False}, 
            update={"$set": {"is_deleted": True} },
            return_document=ReturnDocument.AFTER)
        return deleted_data
    
    def update(self, collection_name: str, old_data_id: str | ObjectId, new_data: Dict):
        if not isinstance(new_data, dict):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")
        old_data_id = self.validate_object_id(old_data_id)

        collection = self.get_collection_data(collection_name)
        updated_data = collection.find_one_and_update(
            filter={"_id": old_data_id, "is_deleted": False }, 
            update={"$set": new_data}, 
            return_document=ReturnDocument.AFTER)
        return updated_data
    
    def get_all_data(self, collection_name: str):
        if not isinstance(collection_name, str):
            raise ValueError("O nome da coleção deve ser uma string")
        collection = self.get_collection_data(collection_name)
        result = collection.find({})

        return result

    def find_by_id(self, collection_name: str, data_id: str | ObjectId):
        if not isinstance(data_id, str) or not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")
        data_id = self.validate_object_id(data_id)

        collection = self.get_collection_data(collection_name)
        result = collection.find_one({
            "_id": data_id,
            "is_deleted": False
        })
        return result

    def find_data_by_key(self, collection_name: str, key: str, key_data: Any):
        if not isinstance(key, str) or not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")

        collection = self.get_collection_data(collection_name)
        
        filter_query = {key: key_data}
        if collection_name in ['users', 'projects']:
            filter_query['is_deleted'] = False
        result = collection.find_one(filter_query)

        return result

    def find_many_data_by_key(self, collection_name: str, key: str, key_data: str):
        if not isinstance(key, str) or not isinstance(collection_name, str):
            raise ValueError("O valor enviado é incorreto pra sua formatação.")

        collection = self.get_collection_data(collection_name)
        
        filter_query = {key: {"$in": key_data}}
        if collection_name in ['users', 'projects']:
            filter_query['is_deleted'] = False
        result = collection.find(filter_query)

        return result

    def validate_object_id(self, id_value: str | ObjectId) -> ObjectId:
        if isinstance(id_value, ObjectId):
            return id_value
        if isinstance(id_value, str) and ObjectId.is_valid(id_value):
            return ObjectId(id_value)
        raise ValueError(f"ID inválido: {id_value}")

