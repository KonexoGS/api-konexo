from app import world_bank_url
from app.utils.formatter import FormatCountry
from app.api.v1.routes import APIRouter
from app.utils.getIndicatorInfo import get_indicator_info, get_indicator_list
from app.utils.translator import Translator
from app.models.indicators_models import IndicatorsModelSchema
from app.models.country_models import CountryAllInfosBaseModel
from fastapi import HTTPException, Query
from fastapi.responses import Response, PlainTextResponse
from fastapi.exceptions import ResponseValidationError
from typing import Annotated, Any, Literal, Dict, List
from requests import Response, request
from datetime import datetime
from traceback import format_exc

router = APIRouter()
iso_codes_default = ["US","CN", "JP", "DE", "IN", "GB", "FR", "BR", "IT", "CA", "RU", "KR", "AU", "MX", "ES", "ID", "SA", "TR", "AR", "ZA"]

@router.get('/infos/country/{country_iso_code}', name='Busque o nome de um país, e retorna todos os dados disponíveis', response_model=CountryAllInfosBaseModel)
def get_country_base_nfo(country_iso_code: str, year: Annotated[str | None, Query(max_length=5)] = None):
    try:
        if len(country_iso_code) > 3 or len(country_iso_code) <= 1:
            raise HTTPException(status_code=400, detail="O código ISO do país deve conter de duas a três caractéres.")

        uri = f'{world_bank_url}/country/{country_iso_code}?format=json'
        response: Response = request('GET', uri)
        country: Any = response.json()


        if len(country) <= 1:
            raise HTTPException(status_code=404, detail='Código ISO do país informado é inválido. Acesse [https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes] para mais informações.')

        details: Dict[str, Any] = {}
        indicators = get_indicator_list().keys()
        for key in indicators:
            details[key] = get_details_from_country(info=key, country_iso_code=country[1][0]['iso2Code'].lower(), year=year).main_values # type: ignore

        return FormatCountry.format_to_details_by_country(country[1], details)
    
    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=Translator.translatePlainText(type_ex.__str__()))
    except HTTPException as http_ex:
        raise HTTPException(detail=http_ex.detail, status_code=http_ex.status_code)
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__getattribute__('detail'), status_code=500)
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")
    
@router.get('/infos/country/{country_iso_code}/{info}', name='Procure sobre os detalhes de um determinado país especificado', response_model=IndicatorsModelSchema | None)
def get_details_from_country(info: Literal["PIB", "Populacao", "Desigualdade(GINI)", "Trabalhadores Agro", "ForcaTotal Trabalho"], country_iso_code: str, year: Annotated[str | None, Query(max_length=5)] = None):
    try:
        if len(country_iso_code) > 3 or len(country_iso_code) <= 1:
            raise HTTPException(status_code=400, detail="O código ISO do país deve conter de duas a três caractéres.")
        
        indicator = get_indicator_info(info)
        
        uri = f'{world_bank_url}/country/{country_iso_code}/indicators/{indicator}?format=json'
        if year and year.isnumeric():
            format_year: int = int(year)
            if format_year <= datetime.now().year:
                uri += f'&date={year}'

        response: Response = request('GET', uri)
        country: Any = response.json()

        if len(country) <= 1:
            error: str = country[0]['message'][0]['value']
            raise HTTPException(status_code=404, detail=Translator.translatePlainText(error))
        
        return FormatCountry.format_to_indicator_model(country[1])
        

    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=Translator.translatePlainText(type_ex.__str__()))
    except HTTPException as http_ex:
        raise http_ex
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")
    
@router.get('/infos/all/{param}', name='Recebe um dado e retorna todas as informações dos 20 principais países', response_model=List[IndicatorsModelSchema])
def get_details_from_all_default_countries(
    param: Literal["PIB", "Populacao", "Desigualdade(GINI)", "Trabalhadores Agro", "ForcaTotal Trabalho"], 
    year: Annotated[str | None, Query(max_length=5)] = None
):
    try:
        all_country_data: List[IndicatorsModelSchema] = []       
        indicator = get_indicator_info(param)
        for iso in iso_codes_default: 
            uri = f'{world_bank_url}/country/{iso}/indicators/{indicator}?format=json'

            if year and year.isnumeric():
                format_year = int(year)
                if format_year <= datetime.now().year:
                    uri += f'&date={year}'

            response: Response = request('GET', uri)
            country: Any = response.json()

            if len(country) <= 1:
                raise HTTPException(status_code=404, detail="Não foi possível localizar o país procurado.")

            model = FormatCountry.format_to_indicator_model(country[1])
            all_country_data.append(model)

        return all_country_data
    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=Translator.translatePlainText(type_ex.__str__()))
    except HTTPException as http_ex:
        raise http_ex
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")
    
@router.get('/infos/calc/{param}/average', name='Recebe um dado e retorna a média dos valores obtidos')
def get_data_average_from_country(
    param: Literal["PIB", "Populacao", "Desigualdade(GINI)", "Trabalhadores Agro", "ForcaTotal Trabalho"], 
    iso_code: Annotated[str | None, Query(max_length=3)] = None
):
    try:
        average: float = 0.0
        count_years: int = 0
        
        if not iso_code:
            countries = get_details_from_all_default_countries(param) 
            total_sum = 0.0
            
            for country in countries:
                valid_values = [data.value for data in country.main_values if data.value is not None]
                total_sum += sum(valid_values)
                count_years += len(valid_values)
                       
            if count_years > 0:
                average = total_sum / count_years 
        
        else:
            countries_data = get_details_from_country(param, iso_code) 
            total_sum = 0.0
            
            valid_values = [data.value for data in countries_data.main_values if data.value is not None]
            total_sum += sum(valid_values)
            count_years += len(valid_values)
            
            if count_years > 0:
                average = total_sum / count_years
        
        return {
            "SearchAll": iso_code is None,
            "AverageType": param,
            "iso_code": iso_code.upper() if iso_c1ode else None,  # type: ignore
            "Average": round(average, 4),
            "YearsCounted": count_years
        }
        

    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=Translator.translatePlainText(type_ex.__str__()))
    except HTTPException as http_ex:
        raise http_ex
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")
    
@router.get('/infos/calc/{param}/variance', name='Recebe um dado e retorna a variância dos valores obtidos')
def get_data_variance_from_country(
    param: Literal["PIB", "Populacao", "Desigualdade(GINI)", "Trabalhadores Agro", "ForcaTotal Trabalho"], 
    iso_code: Annotated[str | None, Query(max_length=3)] = None
):
    from math import pow

    try:
        variance: float = 0.0
        all_values: List[float] = []

        if not iso_code:
            countries = get_details_from_all_default_countries(param) 
            
            for country in countries:
                valid_values = [data.value for data in country.main_values if data.value is not None]
                all_values.extend(valid_values)
        else:
            countries_data = get_details_from_country(param, iso_code) 
            all_values = [data.value for data in countries_data.main_values if data.value is not None]
        
        count_years = len(all_values)
        if count_years < 2:
            raise HTTPException(status_code=400, detail="Não há dados suficientes para calcular a variância.")
        
        average = sum(all_values) / count_years
        sum_pow = 0
        for val in all_values: # type: ignore
            sum_pow += pow((val - average), 2)
            
        variance = sum_pow / (count_years - 1)
        
        return {
            "SearchAll": iso_code is None,
            "AverageType": param,
            "iso_code": iso_code.upper() if iso_code else None,
            "Variance": round(variance, 4),
            "YearsCounted": count_years
        }
        

    except TypeError as type_ex:
        raise HTTPException(status_code=400, detail=Translator.translatePlainText(type_ex.__str__()))
    except HTTPException as http_ex:
        raise http_ex
    except ResponseValidationError as resp_ex:
        raise HTTPException(detail=resp_ex.__str__(), status_code=500)
    except Exception:
        print(format_exc())
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado na busca pelo país")