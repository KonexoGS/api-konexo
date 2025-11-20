from dataclasses import dataclass
from typing import List
from pydantic import Base64Str, BaseModel
from app.enums import ProjectsCategoryAlias


class ProjectsResultModel(BaseModel):
    _id: str
    friendly_code: str | None
    owner_id: str
    project_name: str
    short_description: str
    full_description: str
    category: List[str]
    has_github: bool = False
    github_link: str | None = None
    developers_id: List[str]
    banner_photo: Base64Str | None = None
    is_deleted: bool = False

class ProjectResponseModel(BaseModel):
    owner_id: str
    project_name: str
    short_description: str
    full_description: str
    category: List[ProjectsCategoryAlias]
    has_github: bool = False
    github_link: str | None = None
    developers_id: List[str]