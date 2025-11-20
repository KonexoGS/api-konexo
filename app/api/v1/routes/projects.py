from app.api.v1.routes import APIRouter
from fastapi import HTTPException
from app.enums import ProjectsCategoryAlias
from typing import Literal
from app.service.project_service import ProjectService
from app.models.projects_model import ProjectsModel
from traceback import format_exc
from app.utils.gen_friendlycode import GenerateFriendlyCode
from app.enums import ProjectsCategoryAlias

router = APIRouter()
_project_service = ProjectService()

@router.get("/search/id/{project_id}", name="Procure por um projeto especificando o seu tipo", response_model=ProjectsResultModel)
def get_project_by_id(project_id: str):
    try:
        project = _project_service.find_by_id(collection_name=_project_service.main_collection_name, data_id=project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Nenhum projeto com esse ID foi encontrado")
       
        project["_id"] = str(project["_id"])
        project["owner_id"] = str(project["owner_id"])

        if "developers_id" in project:
            project["developers_id"] = [str(dev) for dev in project["developers_id"]]

        return ProjectsResultModel(**project)

    except HTTPException:
        raise
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=format_exc())
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")
    

@router.get("/search/category/{project_category}", response_model=List[ProjectsResultModel])
def get_projects_by_category(project_category: ProjectsCategoryAlias):
    try:
        projects = _project_service.find_projects_by_category(category=project_category)

        if not projects:
            raise HTTPException(status_code=404, detail=f"Nenhum projeto com a categoria {project_category.upper()} foi encontrado")

        return [
            ProjectsResultModel(
                **{
                    **p,
                    "_id": str(p["_id"]),
                    "owner_id": str(p["owner_id"]),
                    "developers_id": [str(d) for d in p.get("developers_id", [])]
                }
            ) for p in projects
        ]

    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(status_code=400, detail=format_exc())
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Erro ao buscar projetos por categoria.")
    
@router.get("/search/name/{project_name}", name="Procure projetos a partir de seu nome")
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
