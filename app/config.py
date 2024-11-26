from dotenv import load_dotenv
import os

load_dotenv()


DB_HOST = os.getenv('DB_HOST')
DB_USERNAME =  os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

POSTGRESS_DATABASE_URL = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'
print("Postgres URL:", POSTGRESS_DATABASE_URL)
