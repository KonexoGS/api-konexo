from app.core.session import Database
from app.models.connections_model import *
from app.models.developers_model import *
from app.enums import ConnectionStatus
from app.service.user_service import UserService
from app.service.auth_service import AuthService
from fastapi import HTTPException, UploadFile, File, status
from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.typings import _DocumentType
from datetime import datetime


class ConnectionService(Database):
    def __init__(self):
        super().__init__()
        self.default_collection_name: str = "connections"
        self.default_collection: Collection = super().get_collection_data(self.default_collection_name)
    
    def get_connections(self, dev_id: str, conn_status: ConnectionStatus = ConnectionStatus.ACCEPTED) -> List[ConnectionsModel]:
        try:
            all_dev_connections: List[ConnectionsModel] = super().find_many_data_by_key(
                collection_name=self.default_collection_name,
                key="source_dev_id",
                key_data=dev_id
            )
            dev_connections: List[ConnectionsModel] = self.default_collection.find({"status": conn_status.value}).to_list()
            
            return dev_connections
        except HTTPException:
            raise

    def create_connection(self, dev_source_id: str, dev_target_id: str, note: str) -> ConnectionResponseModel:
        try:
            if (self.already_connected(dev_source_id, dev_target_id)):
                raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Já existe uma conexão entre os usuários")

            new_connection = ConnectionsModel(
                source_dev_id=dev_source_id,
                target_dev_id=dev_target_id,
                status=ConnectionStatus.WAITING.value,
                note=note,
                created_on=datetime.now()
            )
            connection_id = super().insert(self.default_collection_name, new_connection.model_dump())
            if not connection_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi possível se conectar com esse usuário")        
            

            return ConnectionResponseModel(
                is_created=connection_id != None,
                conn_id=connection_id,
                target_dev_id=dev_target_id,
                current_status=ConnectionStatus(new_connection.status)
            )
        except HTTPException:
            raise


    def already_connected(self, dev_source_id: str, dev_target_id: str) -> bool:
        connection = self.default_collection.find_one({
            "source_dev_id": dev_source_id,
            "target_dev_id": dev_target_id
        })
        return connection is not None