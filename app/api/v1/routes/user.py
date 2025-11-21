from app.api.v1.routes import APIRouter
from app.models.user_model import *
from app.service.user_service import UserService
from fastapi import HTTPException
from typing import List
from traceback import format_exc

router = APIRouter()

_user_service = UserService()

@router.get('/', name="Procure por todos os usuários do sistema", response_model=List[UserModel])
def get_all_users():
    try:
        users = list(_user_service.get_all_data(_user_service.user_collection_name))
        if not users:
            raise HTTPException(status_code=404, detail="Nenhum Usuários foi encontrado")
        users_normalized = [_user_service.normalize_mongo_document(p) for p in users]

        return users_normalized

    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")

@router.get('/search/{email}', name='Procure por usuários a partir do seu username', response_model=UserModel)
def get_user_by_email(email: str):
    try:
        user = _user_service.find_user_by_login(user_email=email)
        return user
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")