from dataclasses import dataclass
from typing import List, Dict
from pydantic import BaseModel
from bson import ObjectId
from app.models.user_model import UserModel, UserResponseModel
from app.models.badges_model import BadgesModel
from app.enums import DeveloperLevel, LanguageLevel
from datetime import datetime

class ExperienceModel(BaseModel):
    company: str
    role: str
    begin: datetime = datetime.now().date()
    end: datetime | str | None = None
    description: str | None = None

class FormationModel(BaseModel):
    name: str
    institution: str
    completed_year: int
    description: str | None = None

class LanguageModel(BaseModel):
    name: str
    level: str # LanguageLevelEnum


class DevelopersModel(BaseModel):
    dev_id: str | None = None
    tech_skills: List[str]
    user_id: str
    dev_level: DeveloperLevel = DeveloperLevel.BEGINNER.value
    soft_skills: List[str] = []
    experience: List[ExperienceModel] = []
    languages: List[LanguageModel] = [LanguageModel(name="Português", level=LanguageLevel.FLUENT.value)]
    total_experience: int = 0
    projects_id: List[str] = []
    badges_id: List[BadgesModel] = []
    is_recommend: bool = False


class DeveloperResponseModel(UserResponseModel):
    tech_skills: List[str]
    soft_skills: List[str] = []
    dev_level: DeveloperLevel = DeveloperLevel.BEGINNER.value
    experience: List[ExperienceModel] = []
    languages: List[LanguageModel] = [LanguageModel(name="Português", level=LanguageLevel.FLUENT.value)]

