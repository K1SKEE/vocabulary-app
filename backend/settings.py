import os

from dotenv import load_dotenv

load_dotenv()

REAL_DATABASE_URL = os.getenv(
    'DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@db:5432/postgres'
)

SECRET_KEY: str = os.getenv('SECRET_KEY', default='secret_key')

ALGORITHM: str = os.getenv('ALGORITHM', default='HS256')

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',
                                                 default='10'))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS',
                                               default='30'))
