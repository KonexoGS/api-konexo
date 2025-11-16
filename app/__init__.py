from dotenv import load_dotenv
from os import getenv
from database.session import Database

load_dotenv()

db_connection = getenv('DB_CONNECTION')
db_password = getenv('DB_PASSWORD')
world_bank_url = getenv('WORLD_BANK_API')
konexoDb = Database()
