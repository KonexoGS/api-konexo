from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from app.core.session import Database
from app.core.local_db import DatabaseLocal
from app.api.v1.routes import auth, developers, projects, countries
from json import load
from traceback import format_exc

app = FastAPI(title="Konexo API", version='v1')
database = Database()

app.include_router(router=auth.router, prefix='/auth', tags=["OAuth"])
app.include_router(router=developers.router, prefix='/devs', tags=["Desenvolvedores"])
app.include_router(router=countries.router, prefix='/countries', tags=["Informações dos Países"])
app.include_router(router=projects.router, prefix='/projects', tags=["Projetos"])

@app.on_event("startup")
async def lifespan():
    database.start_session()

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

@app.get("/default-profiles/search", name="Retorna usuários padrão do sistema a partir de uma busca filtrada")
def get_default_profiles(username: str = None, name: str = None):
    try:
        if not username and not name:
            raise HTTPException(status_code=400, detail="Ao menos um dos parâmetros devem ser conter valor")

        db = DatabaseLocal()    
        default_users: List[Dict] = db.get_default_users()

        results = []
        if username:
            for user in default_users:
                if username.strip().lower() in user['username'].strip().lower():
                    results.append(user)
        else:
            if name.isnumeric():
                return None
            for user in default_users:
                if name.strip().lower() in user['full_name'].strip().lower():
                    results.append(user)
                
        if len(results) > 0:
            return results
        raise HTTPException(status_code=404, detail="Nenhum usuário foi encontrado.")
                
    except HTTPException:
        raise
    except KeyError:
        print(format_exc())
        raise HTTPException(status_code=404, detail="Parâmeto de busca incorreto.") 
    except Exception as e:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado no sistema")