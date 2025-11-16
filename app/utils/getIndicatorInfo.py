from app.enums import Indicators

def get_indicator_info(info: str):
    indicators = {
        "PIB": Indicators.PIB.value,
        "Populacao": Indicators.POPULATION.value,
        "Desigualdade(GINI)": Indicators.GINI.value,
        "Trabalhadores Agro": Indicators.AGRO.value,
        "ForcaTotal Trabalho": Indicators.WORK.value
    }

    return indicators[info]