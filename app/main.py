from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from app.core.session import Database
from app.core.local_db import DatabaseLocal
from app.api.v1.routes import auth, developers, projects, countries
from json import load

app = FastAPI(title="Konexo API", version='v1')

app.include_router(router=auth.router, prefix='/auth', tags=["OAuth"])
app.include_router(router=developers.router, prefix='/devs', tags=["Desenvolvedores"])
app.include_router(router=countries.router, prefix='/countries', tags=["Informações dos Países"])
app.include_router(router=projects.router, prefix='/projects', tags=["Projetos"])

@app.on_event("startup")
async def lifespan():
    Database().start_session()

@app.get("/default-profiles", name="Retorna usuários padrão do sistema")
def get_default_profiles(result: Any = None):
    try:
        db = DatabaseLocal()
        if result and not result.isnumeric():
            raise HTTPException(status_code=400, detail='Formatação inválida. Informe um número inteiro em resultados')
            
        return db.get_default_users(result)
    except HTTPException:
        raise 
    except Exception:
        raise