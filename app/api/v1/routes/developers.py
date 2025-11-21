from app.api.v1.routes import APIRouter
from fastapi import HTTPException, UploadFile, File
from app.models.user_model import *
from app.models.developers_model import *
from app.service.developer_service import DeveloperService
from app.api.v1.routes.user import get_all_users
from traceback import format_exc

router = APIRouter()
_dev_service = DeveloperService()


@router.get('/', name="Conheça todos os devs do sistema", response_model=List[DeveloperResponseModel])
def get_all_dev():
    try:
        raw_devs = list(_dev_service.get_all_data(_dev_service.dev_colection_name))
        if not raw_devs:
            raise HTTPException(status_code=404, detail="Nenhum usuário foi encontrado.")
        raw_users = get_all_users()

        devs = [_dev_service.normalize_mongo_document(dev) for dev in raw_devs]

        users_dict = {str(user["_id"]): user for user in raw_users}

        results = []

        for dev in devs:
            user_id = str(dev.get("user_id"))

            db_user = users_dict.get(user_id)
            if not db_user:
                continue 

            dev_id = dev.pop("_id")
            merged = DeveloperUserModel(
                dev_id=dev_id,
                **db_user,
                **dev
            )

            results.append(merged)

        return results
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")

@router.get('/search', name='Procure os devs a patir do username ou name2', response_model=List[DevelopersModel])
def get_users_by_filter(username: str | None = None, name: str | None = None): 
    try:
        if not username and not name:
            raise HTTPException(status_code=400, detail="Ao menos um dos parâmetros devem conter valor")

        results = []
        print(_dev_service.user_collection_name)
        if username:
            results = _dev_service.find_many_data_by_key(
                collection_name=_dev_service.user_collection_name,
                key="username",
                key_data=username)
        else:
            results = _dev_service.find_many_data_by_key(
                collection_name=_dev_service.user_collection_name,
                key="full_name",
                key_data=name)


        # results = []
        # if username:
        #     for user in default_users:
        #         if username.strip().lower() in user['username'].strip().lower():
        #             results.append(user)
        # else:
        #     if name.isnumeric():
        #         return None
        #     for user in default_users:
        #         if name.strip().lower() in user['full_name'].strip().lower():
        #             results.append(user)
                
        return DeveloperUserModel(
            dev_id=str(dev_id),
            **db_user, 
            **db_dev)
    except HTTPException: 
        raise
    except KeyError:
        print(format_exc())
        raise HTTPException(status_code=404, detail="Parâmeto de busca incorreto.") 
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado no sistema")

@router.post('/add', name='Adicione um dev desenvolvedor no sistema', response_model=DevelopersModel)
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


@router.put('/{dev_id}/profile_photo', name="Adicione uma nova foto pro seu usuário", response_model=DevelopersModel)
def add_profile_photo(file: UploadFile | None = File(None)):
    pass


@router.get('/profile/{username}', name="Acesse o perfil do usuário pelo username")
def find_user_by_username(username: str):
    try:
        db_user = _dev_service.find_data_by_key(
            collection_name=_dev_service.user_collection_name, 
            key="username",
            key_data=username)
        
        if not db_user:
            raise HTTPException(status_code=404, detail="Nenhum usuário encontrado")
        
        db_dev = _dev_service.find_data_by_key(
            collection_name="developers",
            key="user_id",
            key_data=str(db_user['_id'])
        )

        if not db_dev:
            raise HTTPException(status_code=404, detail="Nenhum desenvolvedor encontrado")

        dev_id = db_dev.pop('_id')

        return DeveloperUserModel(
            dev_id=str(dev_id),
            **db_user, 
            **db_dev)
    except HTTPException:
        print(format_exc())
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")
