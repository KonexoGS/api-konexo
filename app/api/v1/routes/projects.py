from app.api.v1.routes import APIRouter
from fastapi import HTTPException
from app.enums import ProjectsCategoryAlias
from typing import Literal
from app.service.project_service import ProjectService
from app.models.projects_model import ProjectsModel, ProjectsResultModel
from traceback import format_exc

router = APIRouter()
_project_service = ProjectService()

@router.get("/search/{project_id}", name="Procure por um projeto especificando o seu tipo", response_model=ProjectsModel)
def get_project_by_id(project_id: str):
    try:
        project = _project_service.find_by_id(collection_name=main_collection_name, data_id=project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Nenhum projeto com esse ID foi encontrado")
        return project

    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=format_exc())
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")
    

@router.get("/search/{project_category}", name="Procura por projetos partindo de sua categoria", response_model=ProjectsModel)
def get_projects_by_category(project_category: str):
    try:
        projects = _project_service.find_projects_by_category(category=project_category)

        if not projects:
            raise HTTPException(status_code=404, detail=f"Nenhum projeto com a categoria {project_category.upper()} foi encontrado")
        return projects
    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=format_exc())
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")
    
@router.get("/search/{project_name}", name="Procure projetos a partir de seu nome")
def find_project_by_name(project_name: str):
    try:
        projects = _project_service.find_by_project_name(project_name=project_name)

        if not projects:
            raise HTTPException(status_code=404, detail="Nenhum projeto foi encontrado")
        return projects
    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=format_exc())
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")

# rota temporária, o correto é o usuário possuí-la para adicionar na melhor maneira
@router.post("/add", name="Adicione um novo evento na plataforma", response_model=ProjectsResultModel)
def add_new_project(new_project: ProjectsModel):
    try:
        new_project_id = _project_service.insert(
            collection_name=_project_service.main_collection_name,
            new_data=new_project.model_dump())

        if not new_project_id:
            raise HTTPException(status_code=500, detail="Erro ao inserir projeto")

        resolve = ProjectsResultModel(
            _id=str(new_project_id),
            **new_project.dict()
        )
        
        return resolve
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=ex)
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")
