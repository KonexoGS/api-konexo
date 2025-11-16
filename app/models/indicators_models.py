from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass

class IndicatorsValueSchema(BaseModel):
    year: Optional[str] = None
    value: Optional[float] = None

class IndicatorsModelSchema(BaseModel):
    country: str
    iso_code: str
    indicator: str
    main_values: List[IndicatorsValueSchema]
