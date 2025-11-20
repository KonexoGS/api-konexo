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
    PLAIN = '200'
    SENIOR = '205'
    JUNIOR = '210'
    INTERNSHIP = '215'
    BEGINNER = '220'

class Roles(str, Enum):
    FRONT = '300'
    BACK = '305'
    CYBER = '310'
    ENGINEER = '315'
    IOT = '320'
    DATA = '325'
    
class Indicators(str, Enum):
    PIB = 'NY.GDP.PCAP.CD'
    POPULATION = 'SP.POP.TOTL'
    GINI = 'SI.POV.GINI' # Desigualdade
    AGRO = 'SL.AGR.EMPL.ZS'
    WORK = 'SL.TLF.TOTL.IN'

class UserType(str, Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"