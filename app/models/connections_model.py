from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from app.enums import ConnectionStatus

class ConnectionsModel(BaseModel):
    _id: str
    source_dev_id: str | None
    target_dev_id: str | None
    note: str
    status: int
    created_on: datetime = Field(default_factory=datetime.now())


class ConnectionResponseModel(BaseModel):
    is_created: bool
    conn_id: str
    target_dev_id: str
    current_status: str
