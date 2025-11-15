from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class stacks(BaseModel):
    friendly_code: int
    name: str