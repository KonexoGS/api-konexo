from enum import Enum

class ProjectsCategory(str, Enum):
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
    