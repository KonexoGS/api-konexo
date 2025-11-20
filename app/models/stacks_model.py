from pydantic import BaseModel
from dataclasses import dataclass

class Stacks(BaseModel):
    friendly_code: int
    name: str