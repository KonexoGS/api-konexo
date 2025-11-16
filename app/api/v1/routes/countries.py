from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import ResponseValidationError
from app.api.v1.routes import APIRouter
from typing import List, Annotated, Dict, Any
from app import world_bank_url
from requests import Response, request
from app.enums import Indicators
from datetime import datetime
from deep_translator import GoogleTranslator
from app.helpers.formatter import FormatCountry
from app.models.indicators_models import IndicatorsModelSchema
from app.models.country_models import CountryBaseModel

router = APIRouter()
@router.get('/info/{country_iso_code}', name='Busque informações de um país', response_model=CountryBaseModel)
def get_country_base_nfo(country_iso_code: str):
    try:
        if len(country_iso_code) >= 3 or len(country_iso_code) <= 1:
            raise HTTPException(status_code=400, detail="O código ISO do país deve conter de duas a três caractéres.")

        uri = f'{world_bank_url}/country/{country_iso_code}?format=json'
        response: Response = request('GET', uri)
        country: Any = response.json()


        if len(country) <= 1:
            raise HTTPException(status_code=404, detail='Código ISO do país informado é inválido. Acesse [https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes] para mais informações.')

        return FormatCountry.format_to_base_country_model(country[1])
    
    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=GoogleTranslator(source='en', target='pt').translate(type_ex.__str__()))
    except HTTPException as http_ex:
        raise HTTPException(detail=http_ex.detail, status_code=http_ex.status_code)
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={"Unexpected Erro": "Ocorreu um erro inesperado na busca pelo país"})
    
@router.get('/info/pib/{country_iso_code}', name='Procure sobre o PIB de um determinado país do mundo', response_model=IndicatorsModelSchema | None)
def get_pib_from_country(country_iso_code: str, year: Annotated[str | None, Query(max_length=5)] = None):
    try:
        if len(country_iso_code) > 3 or len(country_iso_code) <= 1:
            raise HTTPException(status_code=400, detail="O código ISO do país deve conter de duas a três caractéres.")
        
        indicator = Indicators.PIB.value
        uri = f'{world_bank_url}/country/{country_iso_code}/indicators/{indicator}?format=json'
        if year and year.isnumeric():
            format_year: int = int(year)
            if format_year <= datetime.now().year:
                uri += f'&date={year}'

        response: Response = request('GET', uri)
        country: Any = response.json()

        if len(country) <= 1:
            error: str = country[0]['message'][0]['value']
            raise HTTPException(status_code=404, detail=GoogleTranslator(source='en', target='pt').translate(error))
        
        return FormatCountry.format_to_pib_model(country[1])
        

    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=GoogleTranslator(source='en', target='pt').translate(type_ex.__str__()))
    except HTTPException as http_ex:
        raise http_ex
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")
    
@router.get('/info/population/{country_iso_code}', name="Procure a população do país de um determinado país")
def get_pop_from_country(country_iso_code: str, year: Annotated[str | None, Query(max_length=5)] = None):
    try:
        if len(country_iso_code) > 3 or len(country_iso_code) <= 1:
            raise HTTPException(status_code=400, detail="O código ISO do país deve conter de duas a três caractéres.")
        
        indicator = Indicators.POPULATION.value
        uri = f'{world_bank_url}/country/{country_iso_code}/indicators/{indicator}?format=json'
        if year and year.isnumeric():
            format_year: int = int(year)
            if not format_year < datetime.now().year and format_year < 1975:
                raise HTTPException(status_code=400, detail="Informe um ano válido que seja menor que o atual e maior que 1975")
            uri += f'&date={year}'
            

        response: Response = request('GET', uri)
        country: Any = response.json()

        if len(country) <= 1:
            error: str = country[0]['message'][0]['value']
            raise HTTPException(status_code=404, detail=GoogleTranslator(source='en', target='pt').translate(error))
        
        if country[1] == None:
            if year:
                raise HTTPException(status_code=404, detail="Não foi possível encontrar os dados da população no ano especificado")
            raise HTTPException(status_code=404, detail="Não foi possível encontrar os dados da população")
        
        return FormatCountry.format_to_pib_model(country[1])
        

    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=GoogleTranslator(source='en', target='pt').translate(type_ex.__str__()))
    except HTTPException as http_ex:
        raise http_ex
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")