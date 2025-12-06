from enum import Enum

class ProjectsCategoryCode(str, Enum):
    DEVOPS = '100'
    FRAMEWORK = '105'
    LIBRARY = '110'
    API = '115'
    UIKIT = '120'
    BOT = '125'
    FULLSTACK = '130'
    BACKEND = '135'
    APP = '140'
    SAAS = '145'
    GAME = '150'
    DATABASE = '155'

class ProjectsCategoryAlias(str, Enum):
    NONE = 'none'
    DEVOPS = 'devops'
    FRAMEWORK = 'framework'
    LIBRARY = 'library'
    API = 'api'
    UIKIT = 'uikit'
    BOT = 'bot'
    FULLSTACK = 'fullstack'
    BACKEND = 'backend'
    FRONTEND = 'frontend'
    SAAS = 'saas'
    GAME = 'game'
    DATABASE = 'database'

class DeveloperLevel(str, Enum):
    PLAIN = 'pleno'
    SENIOR = 'senior'
    JUNIOR = 'junior'
    INTERNSHIP = 'estagiário'
    BEGINNER = 'iniciante'

class Roles(str, Enum):
    FRONT = 'front'
    BACK = 'back'
    CYBER = 'cyber'
    ENGINEER = 'engineer'
    IOT = 'iot'
    DATA = 'database'
    
class Indicators(str, Enum):
    PIB = 'NY.GDP.PCAP.CD'
    POPULATION = 'SP.POP.TOTL'
    GINI = 'SI.POV.GINI' # Desigualdade
    AGRO = 'SL.AGR.EMPL.ZS'
    WORK = 'SL.TLF.TOTL.IN'

class UserType(str, Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"
    MARKETING = "marketing"

class LanguageLevel(str, Enum):
    BEGINNER = 'iniciante'
    INTERMEDIATE = 'intermediário'
    ADVANCED_INTERMEDIATE = 'intermediário-avançado'
    ADVANCED = 'avançado'
    FLUENT = 'fluente'

class ConnectionStatus(int, Enum):
    WAITING = 0,
    ACCEPTED = 1,
    REJECTED = 2