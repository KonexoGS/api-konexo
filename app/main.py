from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database.session import Database
from json import load

app = FastAPI(title="Konexo API", version='v1')

@app.on_event("startup")
def on_startup():
    Database.start_session()

@app.get("/default-profiles", name="Retorna usuários padrão do sistema")
def get_default_profiles():
    with ("helper/default_profiles.json", r) as f:
        data = load(f);
    return data