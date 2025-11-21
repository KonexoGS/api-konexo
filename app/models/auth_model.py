from dataclasses import dataclass
from pydantic import NaiveDatetime, BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    username: str