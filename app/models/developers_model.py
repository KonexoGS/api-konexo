from pydantic import BaseModel
from typing import List
from ulid import ULID

class developers(BaseModel):
    _id: ULID
    username: str
    stacks_list: List[int]
    projects_subscribed: List[ULID]
    experience_level: int
    badges: List[int]
    
