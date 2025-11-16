from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass

class CountryBaseModel(BaseModel):
    iso_code: str
    name: str
    capital_city: str
    region: str
    income_level: str
    admin_region: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
