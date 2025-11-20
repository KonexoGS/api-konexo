from dataclasses import dataclass
from typing import List
from pydantic import Base64Str, BaseModel


class ProjectsModel(BaseModel):
    friendly_code: str | None
    owner_id: str
    name: str
    short_description: str
    full_description: str
    category: List[str]
    has_github: bool = False
    developers_id: List[str]
    banner_photo: Base64Str | None
    is_deleted: bool = False

class ProjectsResultModel(ProjectsModel):
    _id: str
