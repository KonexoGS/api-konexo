from dotenv import load_dotenv
from os import getenv

load_dotenv()

db_connection = getenv('DB_CONNECTION')
db_password = getenv('DB_PASSWORD')
world_bank_url = getenv('WORLD_BANK_API')
jwt_secret_key = getenv('SECRET_JWT_KEY')
jwt_encode_algorithm = getenv('ALGORITHM')