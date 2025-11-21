from dataclasses import dataclass
from pydantic import BaseModel

class BadgesModel(BaseModel):
    friendly_code: str
    name: str
    description: str
    required_experience: int
    how_to_get: str