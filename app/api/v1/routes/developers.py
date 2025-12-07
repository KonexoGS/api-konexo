from app.api.v1.routes import APIRouter
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from app.models.user_model import *
from app.models.developers_model import *
from app.service.developer_service import DeveloperService
from app.service.user_service import UserService
from app.service.project_service import ProjectService
from app.api.v1.routes.user import get_all_users
from traceback import format_exc
from pathlib import Path
from mimetypes import guess_type

router = APIRouter()
_dev_service = DeveloperService()
_user_service = UserService()
_project_service = ProjectService()

class ProfilePhotoResponse(BaseModel):
    isValid: bool
    profile_photo: str | None

@router.get('/', name="Conheça todos os devs do sistema", response_model=List[DeveloperResponseModel])
def get_all_devs():
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

@router.get('/search', name='Procure os devs a patir do username ou name2', response_model=List[DeveloperUserModel])
def get_users_by_filter(username: str | None = None, name: str | None = None): 
    try:
        if not username and not name:
            raise HTTPException(status_code=400, detail="Ao menos um dos parâmetros devem conter valor")

        filtered_data = []
        if username:
            filtered_data = _user_service.find_many_data_by_key(
                collection_name=_user_service.user_collection_name,
                key="username",
                key_data=username
            )
        else:
            filtered_data = _user_service.find_many_data_by_key(
                collection_name=_user_service.user_collection_name,
                key="full_name",
                key_data=name or ""
            )

        
        users_dict = {str(user["_id"]): user for user in filtered_data}

        raw_devs = list(_dev_service.get_all_data(_dev_service.dev_colection_name))
        devs = [_dev_service.normalize_mongo_document(dev) for dev in raw_devs]

        results = []
        for dev in devs:
            user_id = str(dev.get("user_id"))
            db_user = users_dict.get(user_id)

            if not db_user:
                continue
            dev_id = dev.pop('_id')
            db_user.pop('_id')
            merged = DeveloperUserModel(
                dev_id=dev_id,
                **db_user,
                **dev
            )
            results.append(merged)

        if not results:
            raise HTTPException(status_code=404, detail="Usuários encontrados não estão registrados como desenvolvedores.")

        return results

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
        new_dev = _dev_service.insert_developer(user_response=new_dev) # type: ignore
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


@router.put('/{dev_id}/profile_photo', name="Adicione uma nova foto pro seu usuário", response_model=ProfilePhotoResponse)
def add_profile_photo(dev_id: str, file: UploadFile):
    try:
        file_name: str = file.filename or ""
        physical_name = f"{dev_id}_{file_name}"

        if not file_name.endswith(('.jpg', '.png', '.jpeg')):
            raise ValueError("Somente jpg, png e jpeg são permidos.")

        dev = _dev_service.find_by_id(
            collection_name=_dev_service.dev_colection_name,
            data_id=dev_id
        )
        
        if not dev:
            raise HTTPException(status_code=404, detail="Desenvolvedor não encontrado")

        updated_user = _user_service.update(
            collection_name=_user_service.user_collection_name,
            old_data_id=dev['user_id'],
            new_data={"profile_photo": file_name}
        )

        path = Path('~/data').expanduser()
        path.mkdir(parents=True, exist_ok=True)

        file_location = path / physical_name
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        return ProfilePhotoResponse(
            isValid=len(updated_user["profile_photo"]) > 0,
            profile_photo=updated_user["profile_photo"]
        )

    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a execução da rota")

@router.get("/{dev_id}/get/profile_photo/", name="Obter foto do usuário", response_class=FileResponse)
def get_profile_photo(dev_id: str):
    try:
        dev = _dev_service.find_by_id(
            collection_name=_dev_service.dev_colection_name,
            data_id=dev_id
        )
        if not dev:
            raise HTTPException(status_code=404, detail="Desenvolvedor não encontrado.")

        user = _user_service.find_by_id(
            collection_name=_user_service.user_collection_name,
            data_id=dev['user_id']
        )

        filename = user.get("profile_photo") # type: ignore
        if not filename:
            raise HTTPException(status_code=404, detail="Usuário não possui nenhuma foto de perfil.")

        path = Path('~/data').expanduser()
        physical_name = f"{dev_id}_{filename}"
        file_path = path / physical_name

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Foto de perfil não encontrada no sistema.")

        mime_type, _ = guess_type(str(file_path))
        if mime_type is None:
            mime_type = "application/octet-stream"

        return FileResponse(
            path=file_path,
            media_type=mime_type,
            filename=filename)
        
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a execução da rota")

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
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo usuário.")

@router.patch('/recommend', name="Recomende um desenvolvedor para outros usuários")
def recommend_dev(dev_id: str, is_recommend: bool = True):
    try:
        if not isinstance(is_recommend, bool):
            raise ValueError("is_recommend deve ser um booleano")

        dev = _dev_service.find_by_id(
            collection_name=_dev_service.dev_colection_name,
            data_id=dev_id
        )

        if not dev:
            raise HTTPException(status_code=404, detail="Desenvolvedor não encontrado no banco")
        
        dev['is_recommend'] = is_recommend

        updated = _dev_service.update(
            collection_name=_dev_service.dev_colection_name,
            old_data_id=dev['_id'],
            new_data=dev
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Desenvolvedor não adicionado no banco")

        dev.pop('_id')

        return dev

    except HTTPException:
        print(format_exc())
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")

@router.get(
    "/projects/{owner_id}",
    name="Buscar todos os projetos de um proprietário",
)
def get_projects_by_owner(owner_id: str):
    try:
        projects = _project_service.find_projects_by_owner(owner_id)

        if not projects:
            raise HTTPException(status_code=404, detail="Nenhum projeto encontrado para esse owner_id")

        projects = [_project_service.normalize_mongo_document(p) for p in projects]

        return projects

    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Erro interno ao buscar projetos do owner")
