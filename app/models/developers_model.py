from dataclasses import dataclass
from typing import List, Dict
from pydantic import NaiveDatetime


@dataclass
class Developers():
    friendly_code: str
    email: str
    username: str
    password: str
    full_name: str
    stacks: List[int]
    role: List[str] 
    level: str
    projects_subscribed: List[str]
    experience_level: int
    badges: List[int]
    is_deleted: bool
    social_medias: Dict[str, str]
    created_at: NaiveDatetime

