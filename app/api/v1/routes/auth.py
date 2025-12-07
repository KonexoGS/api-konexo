from app.api.v1.routes import APIRouter
from app.models.auth_model import TokenData, SimpleOAuthResponseForm
from app.service.auth_service import AuthService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from traceback import format_exc

router = APIRouter()

_auth_service = AuthService()

@router.post('/token', name="Login for access token", description="Informe o email e senha do usuáruio para obter o token de acesso", response_model=TokenData)
def login_for_access_token(form_data: Annotated[SimpleOAuthResponseForm, Depends()]):
    try:
        user = _auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha estão incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=_auth_service.token_expire_minutes)
        access_token = _auth_service.create_access_token(data={"sub": str(user['_id'])}, expires_delta=access_token_expires)

        return TokenData(access_token=access_token, token_type="bearer", username=user['username'], user_id=str(user["_id"]))
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")