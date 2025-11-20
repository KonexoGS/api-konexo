from app.api.v1.routes import APIRouter
from fastapi import HTTPException
from app.enums import ProjectsCategoryAlias
from typing import Literal
from app.service.project_service import ProjectService
from app.models.projects_model import ProjectsResultModel, ProjectResponseModel
from traceback import format_exc
from app.utils.gen_friendlycode import GenerateFriendlyCode
from typing import List, Optional

router = APIRouter()
_project_service = ProjectService()

@router.get("/search", name="Procure por um projeto a partir do seu ID, categoria, ou Nome!", response_model=List[ProjectResponseModel])
def find_projects_from_db(project_id: Optional[str | None] = None, name: Optional[str | None] = None, category: Optional[ProjectsCategoryAlias | None] = None):
    try:
        if not (project_id or name or category):
            raise HTTPException(status_code=400, detail="Especifique pelo menos um dos parâmetros")
        
        response = None
        if project_id:
            response = [_project_service.find_by_id(project_id, _project_service.main_collection_name)]
        elif name:
            response = _project_service.find_by_project_name(project_name=name)
        else:
            response = _project_service.find_projects_by_category(category)

        if len(response) == 0:
            raise HTTPException(status_code=404, detail="Nenhum projeto foi encontrado")    
        return response
    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=format_exc())
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
