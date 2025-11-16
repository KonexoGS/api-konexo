from dataclasses import dataclass
from typing import List
from pydantic import Base64Str


@dataclass
class Projects():
    friendly_code: str
    owner_id: str
    name: str
    short_description: str
    full_description: str
    category: List[str]
    has_github: bool
    developers_ids: List[str]
    banner_photo: Base64Str
    is_deleted: bool
