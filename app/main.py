from fastapi.security import HTTPBearer
from uvicorn import run
from fastapi import FastAPI, Depends
from app.core.session import Database
from app.core.local_db import DatabaseLocal
from app.api.v1.routes import auth, developers, projects, user, connections
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


app = FastAPI(title="Konexo API", version='v1')
oauth2_scheme = HTTPBearer(bearerFormat="Bearer {token}", description="Obtenha o token de acesso em /auth/token e insira aqui para usar a API", scheme_name="Konexo Authorize")
database = Database()

app.include_router(router=auth.router, prefix='/auth', tags=["OAuth"])
app.include_router(router=user.router, prefix='/user', tags=["Usuários"], dependencies=[Depends(oauth2_scheme)])
app.include_router(router=connections.router, prefix="/connect", tags=["Connections"], dependencies=[Depends(oauth2_scheme)])
app.include_router(router=developers.router, prefix='/devs', tags=["Desenvolvedores"], dependencies=[Depends(oauth2_scheme)])
app.include_router(router=projects.router, prefix='/projects', tags=["Projetos"], dependencies=[Depends(oauth2_scheme)])

@app.on_event("startup")
async def lifespan():
    database.start_session()

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)