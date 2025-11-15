from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.database.session import Database
from json import load

app = FastAPI(title="Konexo API", version='v1')

@app.on_event("startup")
def on_startup():
    Database().start_session()

@app.get("/default-profiles", name="Retorna usuários padrão do sistema")
def get_default_profiles(result: str = '50'):
    try:
        if not result.isnumeric():
            raise HTTPException(status_code=400, detail='Formatação inválida. Informe um número inteiro em resultados')
        result = int(result)

        with open('app/helpers/default_profiles.json', 'r') as f:
            data: dict = load(f);
        if result == 50:
            return data
        devs: list = []
        keys: list = list(data.keys())
        for i in range(result):
            devs.append(data[keys[i]])
        return devs
    except HTTPException:
        raise 
    except Exception as e:
        raise