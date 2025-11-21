import jwt
from app.core.session import Database
from app.service.user_service import UserService
from datetime import datetime, timedelta, timezone
from typing import Annotated
from pydantic import BaseModel, ValidationError
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pwdlib import PasswordHash



class AuthService(Database):
    def __init__():
        super().__init__()
        self.password_hash = PasswordHash.recommended()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.user_service = UserService()


    def verify_password(self, plain_password: str, hashed_password: str):
        return password_hash.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str):
        return password_hash.hash(password)

    def authenticate_user(self, password: str, username: str | None = None, email: str | None = None):
        user = self.user
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
