from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from app.models.indicators_models import IndicatorsValueSchema

class CountryBaseModel(BaseModel):
    iso_code: str
    name: str
    capital_city: str
    region: str
    income_level: str
    admin_region: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]


class CountryAllInfosBaseModel(BaseModel):
    base_info: CountryBaseModel
    pib_values: List[IndicatorsValueSchema]
    population_values: List[IndicatorsValueSchema]
    gni_values: List[IndicatorsValueSchema]
    agro_work: List[IndicatorsValueSchema]
    effort_work: List[IndicatorsValueSchema]
