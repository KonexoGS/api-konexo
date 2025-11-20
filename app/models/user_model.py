from datetime import datetime

class User(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    user_type: str # UserType Enum
    level: str
    projects_subscribed: List[str]
    experience_level: int
    badges: List[int]
    is_deleted: bool
    social_medias: Dict[str, str]
    created_at: datetime


class UserInDB(User):
    hashed_password: str
