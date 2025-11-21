from app.api.v1.routes import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.enums import ProjectsCategoryAlias
from typing import Literal
from app.service.project_service import ProjectService
from app.models.projects_model import *
from traceback import format_exc
from app.utils.gen_friendlycode import GenerateFriendlyCode
from app.utils.translator import Translator
from app.utils.convert_enum import convert_enums_to_values
from typing import List, Optional, Dict, Any

router = APIRouter()
_project_service = ProjectService()

@router.get("/", name="Busque por todos os projetos salvos no banco", response_model=List[ProjectResponseModel])
def get_all_projects():
    try:
        projects = list(_project_service.get_all_data(_project_service.main_collection_name))
        if not projects:
            raise HTTPException(status_code=404, detail="Nenhum Projeto foi encontrado")
        projects_normalized = [_project_service.normalize_mongo_document(p) for p in projects]

        return projects_normalized

    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=format_exc())
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")

@router.get("/search", name="Procure por um projeto a partir do seu ID, categoria, ou Nome!", response_model=List[ProjectResponseSearchModel])
def find_projects_from_db(project_id: Optional[str | None] = None, name: Optional[str | None] = None, category: Optional[ProjectsCategoryAlias | None] = None):
    try:
        if not (project_id or name or category):
            raise HTTPException(status_code=400, detail="Especifique pelo menos um dos parâmetros")
        
        translator = Translator()

        response = None
        if project_id:
            response = [_project_service.find_by_id(data_id=project_id, collection_name=_project_service.main_collection_name)]
            response[0]['_id'] = str(response[0]['_id'])
            response[0]['owner_id'] = str(response[0]['owner_id'])
        elif name:
            response = _project_service.find_by_project_name(project_name=name)
        else:
            response = _project_service.find_projects_by_category(category)

        if len(response) == 0:
            raise HTTPException(status_code=404, detail="Nenhum projeto foi encontrado")    

        projects = []
        for p in response:
            tmp = ProjectResponseSearchModel(
                owner_name=_project_service.find_by_id(collection_name="users", data_id=p['owner_id'])['full_name'],
                **p
            )
            # tmp.short_description = translator.translatePlainText(p['short_description']),
            # tmp.full_description = translator.translatePlainText(p['full_description']),
            projects.append(tmp)

        return projects
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")


@router.post("/add", name="Adicione um novo evento na plataforma", response_model=ProjectsResultModel)
def add_new_project(new_project: ProjectResponseModel):
    try:
        generator = GenerateFriendlyCode()
        project_as_dict = new_project.model_dump()

        project_model = ProjectsResultModel(
            _id="",
            friendly_code=generator.generate_project_code(project_as_dict['category']),
            **project_as_dict
        )

        new_project_id = _project_service.insert_project(
            new_data=project_model.model_dump())

        if not new_project_id:
            raise HTTPException(status_code=500, detail="Erro ao inserir projeto")
        
        project_model._id = new_project_id
        return project_model

    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")


@router.delete('/{project_id}', name="Exclua permanentemente um projeto do sistema a partir do seu ID", response_model=Dict[str, Any])
def delete_project_by_id(project_id: str):
    try:
        if project_id.isnumeric():
            raise HTTPException(status_code=400, detail=f"O Id {project_id} informado é inválido.")
        validated_id = _project_service.validate_object_id(project_id)

        deleted_project = _project_service.hard_delete(
            collection_name=_project_service.main_collection_name, 
            data_id=validated_id)
        
        if not deleted_project:
            raise HTTPException(status_code=404, detail=f"Nenhum projeto com o ID {project_id} foi encontrado.")

        return {
            "has_deleted": len(deleted_project) > 0,
            "message": "Projeto excluído permanentemente com sucesso!",
            "project_id": str(deleted_project['_id'])

        }
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")

@router.patch(
    path='/{project_id}/deactivate', 
    name="Remova o projeto da visualização mas tenha o seus dados salvos no banco", 
    response_model=Dict[str, Any], 
    description="Desativa o projeto do sistema a partir do ID informado na rota. Os dados permamanecem no banco como histórico e possíveis restaurações.")
def deactivate_project_by_id(project_id: str):
    try:
        if project_id.isnumeric():
            raise HTTPException(status_code=400, detail=f"O Id {project_id} informado é inválido.")
        validated_id = _project_service.validate_object_id(project_id)

        deleted_project = _project_service.delete(
            collection_name=_project_service.main_collection_name, 
            data_id=validated_id)
        
        if not deleted_project:
            raise HTTPException(status_code=404, detail=f"Nenhum projeto com o ID {project_id} foi encontrado.")

        return {
            "has_deleted": len(deleted_project) > 0,
            "message": "Projeto excluído com sucesso!",
            "project_id": str(deleted_project['_id'])

        }
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")


@router.put(
    path='/{project_id}/update',
    name="Atualize o conteúdo de um projeto a partir do seu ID",
    response_model=ProjectsResultModel,
    description="Informe o ID de um projeto e atualize as suas informações"
)
def update_project(project_id: str, new_data: ProjectUpdateModel):
    try:
        project_as_dict = new_data.model_dump(exclude_unset=True)
        project_as_dict = convert_enums_to_values(project_as_dict)

        for key, value in list(project_as_dict.items()):
            if isinstance(value, bool):
                continue
            if value == "string":
                project_as_dict.pop(key)
            elif isinstance(value, list) and value and (value[0] in ["string", "none"]):
                project_as_dict.pop(key)

        if len(project_as_dict) == 0:
            raise HTTPException(status_code=400, detail="Nenhuma nova informação foi informada.")

        updated_project = _project_service.update(
            collection_name=_project_service.main_collection_name,
            old_data_id=project_id,
            new_data=project_as_dict
        )

        if not updated_project:
            raise HTTPException(status_code=404, detail="Projeto não foi encontrado")

        updated_project['_id'] = str(updated_project['_id'])
        updated_project['owner_id'] = str(updated_project['owner_id'])
        updated_project['developers_id'] = [str(dev_id) for dev_id in updated_project.get('developers_id', [])]

        updated_project['has_github'] = 'github.com' in updated_project.get('github_link', '')
        return ProjectsResultModel(
            **updated_project
        )

    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a atualização do projeto.")
