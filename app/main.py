from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from app.database.session import Database
from json import load

app = FastAPI(title="Konexo API", version='v1')

@app.on_event("startup")
def on_startup():
    Database().start_session()

@app.get("/default-profiles", name="Retorna usuários padrão do sistema")
def get_default_profiles(result: Any = '50'):
    try:
        if not result.isnumeric():
            raise HTTPException(status_code=400, detail='Formatação inválida. Informe um número inteiro em resultados')
        result = int(result)

        with open('app/local/default_profiles.json', 'r') as f:
            data: Dict[str, Dict[str, str]] = load(f);
        if result == 50:
            return data
        devs: List[Dict[str, str]]  = []
        keys: List[str] = list(data.keys())
        for i in range(result):
            devs.append(data[keys[i]])
        return devs
    except HTTPException:
        raise 
    except Exception:
        raise