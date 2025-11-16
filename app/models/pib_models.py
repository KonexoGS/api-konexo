from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass

class PibValueSchema(BaseModel):
    year: Optional[str] = None
    value: Optional[float] = None

class PibModelSchema(BaseModel):
    country: str
    iso_code: str
    indicator: str
    pib_values: List[PibValueSchema]
