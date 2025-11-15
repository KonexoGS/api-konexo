from pydantic import BaseModel
from ulid import ULID

class stacks(BaseModel):
    _id: ULID
    code: int
    name: str