from dataclasses import dataclass
from pydantic import NaiveDatetime, BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    username: str
    user_id: str

class SimpleOAuthResponseForm(BaseModel):
    username: str
    password: str