from dataclasses import dataclass
from typing import List, Dict
from pydantic import BaseModel
from bson import ObjectId
from app.models.user_model import UserModel, UserResponseModel
from app.models.badges_model import BadgesModel

class DevelopersModel(BaseModel):
    dev_id: str = ""
    stacks: List[str]
    speciality: List[str]
    user_id: str
    level: int = 0
    total_experience: int = 0
    projects_id: List[str] = []
    badges_id: List[BadgesModel] = []


class DeveloperResponseModel(UserResponseModel):
    stacks: List[str]
    speciality: List[str]
