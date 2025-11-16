from typing import List, Dict, Any
from app.models.indicators_models import IndicatorsModelSchema, IndicatorsValueSchema
from app.models.country_models import CountryBaseModel, CountryAllInfosBaseModel


class FormatCountry:

    @staticmethod
    def __format_to_indicator_value(countries: List[Dict[str, Any]]) -> List[IndicatorsValueSchema]:
        return [
            IndicatorsValueSchema(year=country.get('date'), value=country.get('value')) for country in countries
        ]

    @staticmethod
    def format_to_indicator_model(countries: List[Dict[str, Any]]) -> IndicatorsModelSchema:
        main_values = FormatCountry.__format_to_indicator_value(countries)

        return IndicatorsModelSchema(country=countries[0]['country']['value'], iso_code=countries[0]['countryiso3code'], indicator=countries[0]['indicator']['value'],   main_values=main_values)

    @staticmethod
    def __format_to_base_country_model(country: List[Dict[str, Any]]) -> CountryBaseModel:
        data: Dict[str, Any] = country[0]
        isocode: Any = data.get('iso2Code') or data.get('countryiso3code')

        region = data.get('region') or {}
        income = data.get('incomeLevel') or {}
        admin = data.get('adminregion') or {}

        return CountryBaseModel(
            iso_code=isocode,
            name=data.get('name', ''),
            capital_city=data.get('capitalCity', ''),
            region=f"{region.get('value', '')} - {region.get('iso2code', '')}",
            income_level=f"{income.get('value', '')} - {income.get('iso2code', '')}",
            admin_region=(
                f"{admin.get('value', '')} - {admin.get('iso2code', '')}"
                if admin.get('value') or admin.get('iso2code') else None
            ),
            longitude=float(data['longitude']) if data.get('longitude') else None,
            latitude=float(data['latitude']) if data.get('latitude') else None,
        )

    @staticmethod
    def format_to_details_by_country(
        countries: List[Dict[str, Any]],
        countryDetails: Dict[str, List[IndicatorsValueSchema]]
    ) -> CountryAllInfosBaseModel:
        countryBase: CountryBaseModel = FormatCountry.__format_to_base_country_model(countries)

        return CountryAllInfosBaseModel(
            base_info=countryBase,
            pib_values=countryDetails.get('PIB', []),
            population_values=countryDetails.get('Populacao', []),
            gni_values=countryDetails.get('Desigualdade(GINI)', []),
            agro_work=countryDetails.get('Trabalhadores Agro', []),
            effort_work=countryDetails.get('ForcaTotal Trabalho', [])
        )
