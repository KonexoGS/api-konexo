from dataclasses import dataclass
from typing import List, Dict
from pydantic import BaseModel
from bson import ObjectId


class Developers(BaseModel):
    stacks: List[int]
    speciality: List[str]
    level: str
    user_id: ObjectId

