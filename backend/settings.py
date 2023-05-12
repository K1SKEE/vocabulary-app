import os

from dotenv import load_dotenv

load_dotenv()

REAL_DATABASE_URL: str = os.getenv(
    'DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@db:5432/postgres'
)

REDIS_URL: str = os.getenv(
    'REDIS_URL',
    default='redis://:@localhost:6379'
)

EMAIL_CONFIG: dict = {
    'EMAIL_LOGIN': os.getenv('EMAIL_LOGIN', default='example@gmail.com'),
    'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD', default='password-example'),
    'SMTP_SERVER': os.getenv('SMTP_SERVER', default='smtp.gmail.com'),
    'SMTP_PORT': int(os.getenv('SMTP_PORT', default=587))
}

SECRET_KEY: str = os.getenv('SECRET_KEY', default='secret_key')

ALGORITHM: str = os.getenv('ALGORITHM', default='HS256')

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',
                                                 default='10'))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS',
                                               default='30'))
