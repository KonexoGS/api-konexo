from pydantic import BaseModel
from ulid import ULID
from typing import Literal

class projects(BaseModel):
    _id: ULID
    name: str
    description: str
    category: Literal[""]