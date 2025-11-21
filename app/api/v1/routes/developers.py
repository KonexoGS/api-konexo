from app.api.v1.routes import APIRouter
from fastapi import HTTPException
from app.models.user_model import *
from app.models.developers_model import *
from app.service.developer_service import DeveloperService
from traceback import format_exc

router = APIRouter()
_dev_service = DeveloperService()

@router.post('/add', name='Adicione um novo desenvolvedor no sistema', response_model=DevelopersModel)
def add_new_user(new_dev: DeveloperResponseModel):
    try:
        new_dev = _dev_service.insert_developer(new_dev)
        if not new_dev:
            raise HTTPException(status_code=400, detail="Não foi possível adicionar o usuário")
        
        return new_dev
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")