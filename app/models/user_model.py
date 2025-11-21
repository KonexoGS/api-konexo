from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List

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

class UserModel(BaseModel):
    user_id: str = ""
    full_name: str
    username: str
    email: str
    password: str
    headline: str
    address: str
    user_type: str # UserType Enum
    formation: List[FormationModel] = []
    experience: List[ExperienceModel] = []
    is_deleted: bool = False
    social_medias: Dict[str, str] = {}
    profile_photo: str | None = None
    created_at: datetime = datetime.now()


class UserResponseModel(BaseModel):
    full_name: str
    username: str
    headline: str
    address: str
    email: str
    password: str
    formation: List[FormationModel] = []
    experience: List[ExperienceModel] = []
    social_medias: Dict[str, str] = {}