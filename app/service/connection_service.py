from app.core.session import Database
from app.models.connections_model import *
from app.service.developer_service import DeveloperService
from app.models.developers_model import *
from app.enums import ConnectionStatus
from fastapi import HTTPException, status
from typing import List, Any
from pymongo.collection import Collection
from datetime import datetime

_dev_service = DeveloperService()

class ConnectionService(Database):
    def __init__(self):
        super().__init__()
        self.default_collection_name: str = "connections"
        self.default_collection: Collection = super().get_collection_data(self.default_collection_name)
    
    def get_connections(self, dev_id: str, conn_status: ConnectionStatus = ConnectionStatus.ACCEPTED) -> List[ShowConnectionsModel]:
        try:
            dev_connections = self.default_collection.aggregate([
                {
                    "$match": {
                        "$or": [
                            {"source_dev_id": dev_id},
                            {"target_dev_id": dev_id}
                        ],
                        "status": conn_status.value
                    }
                }
            ]).to_list()
            

            result = []
            default_user = _dev_service.find_user_by_dev_id(dev_id)
            for connection in dev_connections:
                source_user = _dev_service.find_user_by_dev_id(connection["source_dev_id"])
                target_user = _dev_service.find_user_by_dev_id(connection["target_dev_id"])

                result.append(ShowConnectionsModel(
                    username = default_user.username,
                    dev_id = dev_id,
                    connected_username = source_user.username if default_user.user_id == source_user.user_id else target_user.username,
                    connected_dev_id = source_user._id or "" if default_user.user_id == source_user.user_id else target_user._id or "",
                    status = ConnectionStatus(connection["status"])
                ))
            
            return result

        except HTTPException:
            raise

    def create_connection(self, dev_source_id: str, dev_target_id: str, note: str | None) -> ConnectionResponseModel:
        try:
            if (self.already_connected(dev_source_id, dev_target_id)):
                raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Já existe uma conexão entre os usuários")

            new_connection = ConnectionsModel(
                source_dev_id=dev_source_id,
                target_dev_id=dev_target_id,
                status=ConnectionStatus.WAITING.value, # type: ignore
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
                current_status=ConnectionStatus(new_connection.status).name
            )
        except HTTPException:
            raise


    def already_connected(self, dev_source_id: str, dev_target_id: str) -> bool:
        connection = self.default_collection.find_one({
            "$or": [
                {
                    "source_dev_id": dev_source_id,
                    "target_dev_id": dev_target_id
                },
                {
                    "source_dev_id": dev_target_id,
                    "target_dev_id": dev_source_id
                }
            ]
        })
        return connection is not None