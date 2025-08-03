import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class BaseConfig(BaseSettings):
    APP_NAME: str = 'Transaction HUB'
    DEBUG: bool = False

    # SQLAlchemy
    DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URI')
    SYNC_DATABASE_URL: str = os.getenv('SYNC_SQLALCHEMY_DATABASE_URI')

    class Config:
        env_file = '.env'


class ProdConfig(BaseConfig):
    DEBUG: bool = False


class DevConfig(BaseConfig):
    DEBUG: bool = True


class TestConfig(BaseConfig):
    DEBUG: bool = True


@lru_cache
def get_settings():
    env = os.getenv('ENVIRONMENT', 'development')

    if env == 'production':
        return ProdConfig()
    elif env == 'testing':
        return TestConfig()

    return DevConfig()
