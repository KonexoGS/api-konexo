from dotenv import load_dotenv
from os import getenv

load_dotenv()

db_connection = getenv('DB_CONNECTION')
db_password = getenv('DB_PASSWORD')
