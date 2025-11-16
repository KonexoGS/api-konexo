from app.enums import Indicators

indicators = {
    "PIB": Indicators.PIB.value,
    "Populacao": Indicators.POPULATION.value,
    "Desigualdade(GINI)": Indicators.GINI.value,
    "Trabalhadores Agro": Indicators.AGRO.value,
    "ForcaTotal Trabalho": Indicators.WORK.value
}
def get_indicator_info(info: str):
    return indicators[info]

def get_indicator_list():
    return indicators