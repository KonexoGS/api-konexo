from app.api.v1.routes import APIRouter
from app.models.user_model import *
from app.service.user_service import UserService
from fastapi import HTTPException

router = APIRouter()

_user_service = UserService()

@router.get('/', name="Procure por todos os usuários do sistema")
def get_all_users():
    pass

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