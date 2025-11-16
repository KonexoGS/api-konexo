from typing import List, Dict, Any
from app.models.indicators_models import IndicatorsModelSchema, IndicatorsValueSchema
from app.models.country_models import CountryBaseModel


class FormatCountry:

    @staticmethod
    def format_to_pib_model(countries: List[Dict[str, Any]]) -> IndicatorsModelSchema:
        main_values = [
            IndicatorsValueSchema(year=country.get('date'), value=country.get('value')) for country in countries
        ]

        return IndicatorsModelSchema(country=countries[0]['country']['value'], iso_code=countries[0]['countryiso3code'], indicator=countries[0]['indicator']['value'],   main_values=main_values)

    @staticmethod
    def format_to_base_country_model(country: List[Dict[str, Any]]) -> CountryBaseModel:
        data = country[0]
        return CountryBaseModel(
            iso_code=data['iso2Code'],
            name=data['name'],
            capital_city=data['capitalCity'],
            region=f"{data['region']['value']} - {data['region']['iso2code']}",
            income_level=f"{data['incomeLevel']['value']} - {data['incomeLevel']['iso2code']}",
            admin_region=f"{data['adminregion']['value']} - {data['adminregion']['iso2code']}",
            longitude=float(data['longitude']) if data['longitude'] else None,
            latitude=float(data['latitude']) if data['latitude'] else None,
        )
