from uvicorn import run
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from app.core.session import Database
from app.core.local_db import DatabaseLocal
from app.api.v1.routes import auth, developers, projects, user, connections
from json import load
from traceback import format_exc

app = FastAPI(title="Konexo API", version='v1')
database = Database()

app.include_router(router=auth.router, prefix='/auth', tags=["OAuth"])
app.include_router(router=user.router, prefix='/user', tags=["Usuários"])
app.include_router(router=connections.router, prefix="/connect", tags=["Connections"])
app.include_router(router=developers.router, prefix='/devs', tags=["Desenvolvedores"])
app.include_router(router=projects.router, prefix='/projects', tags=["Projetos"])

@app.on_event("startup")
async def lifespan():
    database.start_session()


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)