import jwt
from app.core.session import Database
from app.service.user_service import UserService
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pwdlib import PasswordHash
from app import jwt_secret_key, jwt_encode_algorithm
from app.models.auth_model import Token, TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService(Database):
    def __init__(self):
        super().__init__()
        self.password_hash = PasswordHash.recommended()
        self._user_service = UserService()
        self.token_expire_minutes = 60

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.password_hash.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str):
        return self.password_hash.hash(password)

    def authenticate_user(self, username: str | None, password: str):
        user = self._user_service.find_user_by_login(user_email=username)

        if not self.verify_password(password, user['password']):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=jwt_encode_algorithm)
        return encoded_jwt
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Não foi possivel validar a credencial",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_encode_algorithm]) # type: ignore
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception

        user = self._user_service.find_user_by_login(user_email=username)
        if user is None:
            raise credentials_exception
        return user
