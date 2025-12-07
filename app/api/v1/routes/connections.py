from app.api.v1.routes import APIRouter
from app.service.developer_service import DeveloperService
from app.service.connection_service import ConnectionService, ConnectionStatus, ConnectionResponseModel, ConnectionsModel
from fastapi import HTTPException, status
from typing import List
from traceback import format_exc

router = APIRouter()
_dev_service = DeveloperService()
_conn_service = ConnectionService()

@router.get("/{dev_id}", name="Descubra com quem o usuário informado se conectou", response_model=List[ConnectionsModel], status_code=status.HTTP_200_OK)
def get_connections_from_dev_id(dev_id: str):
    try:
        dev = _dev_service.find_by_id(_dev_service.dev_colection_name, dev_id)
        if not dev:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi possivel encontrar o dev")
        connection_accepted = _conn_service.get_connections(
            dev_id=dev_id,
            conn_status=ConnectionStatus.ACCEPTED
        )
        return connection_accepted

    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")
    
@router.post("/", name="Conecte-se com outro usuário da plataforma", response_model=ConnectionResponseModel, status_code=status.HTTP_201_CREATED)
def create_connection(dev_source_id: str, dev_target_id: str, note: str | None = None):
    try:
        dev_ids = [dev_source_id, dev_target_id]
        for idx in dev_ids:
            if (not _dev_service.is_developer_exist(idx)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi possível encontrar o dev solictiado")
        
        connection_result = _conn_service.create_connection(
            dev_source_id=str(dev_source_id),
            dev_target_id=str(dev_target_id),
            note=note
        )
        return connection_result
    except HTTPException:
        raise
    except ValueError as ex:
        print(format_exc())
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado durante a busca pelo projeto.")   