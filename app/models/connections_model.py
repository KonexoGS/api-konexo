from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime
from app.enums import ConnectionStatus

class ConnectionsModel(BaseModel):
    source_dev_id: str | None
    target_dev_id: str | None
    note: str | None = None
    status: ConnectionStatus = ConnectionStatus.WAITING
    created_on: datetime = Field(default_factory = datetime.now)


class ConnectionResponseModel(BaseModel):
    is_created: bool
    conn_id: str
    target_dev_id: str
    current_status: str

class ShowConnectionsModel(BaseModel):
    username: str
    dev_id: str
    connected_username: str
    connected_dev_id: str
    status: ConnectionStatus