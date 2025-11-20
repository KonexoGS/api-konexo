from dataclasses import dataclass
from typing import List
from pydantic import Base64Str, BaseModel


class ProjectsModel(BaseModel):
    friendly_code: str
    owner_id: str
    name: str
    short_description: str
    full_description: str
    category: List[str]
    has_github: bool
    developers_id: List[str]
    banner_photo: Base64Str
    is_deleted: bool

class ProjectsResultModel(ProjectsModel):
    _id: str
