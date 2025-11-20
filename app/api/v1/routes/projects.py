from app.api.v1.routes import APIRouter
from fastapi import HTTPException
from app.enums import ProjectsCategoryAlias
from typing import Literal
from app.service.project_service import ProjectService
from app.models.projects_model import ProjectsModel
from traceback import format_exc

router = APIRouter()
_project_service = ProjectService()

@router.get("/search/{project_id}", name="Procure por um projeto especificando o seu tipo", response_model=ProjectsModel)
def get_project_by__id(project_id: str):
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
    

