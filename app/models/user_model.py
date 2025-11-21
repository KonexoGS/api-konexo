from datetime import datetime
from pydantic import BaseModel
from typing import Dict

class UserModel(BaseModel):
    user_id: str = ""
    full_name: str
    username: str
    email: str
    password: str
    headline: str
    address: str
    user_type: str # UserType Enum
    is_deleted: bool = False
    social_medias: Dict[str, str] = {}
    profile_photo: str
    created_at: datetime = datetime.now()


class UserResponseModel(BaseModel):
    full_name: str
    username: str
    headline: str
    address: str
    email: str
    social_medias: Dict[str, str] = {}