from dataclasses import dataclass
from typing import List, Optional
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
    stacks: List[str]
    has_github: bool = False
    github_link: str | None = None
    developers_id: List[str]
    banner_photo: str | None = None
    is_deleted: bool = False

class ProjectResponseModel(BaseModel):
    owner_id: str
    project_name: str
    short_description: str
    full_description: str
    stacks: List[str]
    category: List[ProjectsCategoryAlias]
    github_link: str | None = None
    developers_id: List[str]

class ProjectUpdateModel(BaseModel):
    project_name: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    stacks: List[str]
    category: Optional[List[ProjectsCategoryAlias]] = None
    github_link: Optional[str] | None = None
    developers_id: Optional[List[str]] = None