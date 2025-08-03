"""Module for managing dependency injections."""

import os

from dependency_injector import containers, providers
from dotenv import load_dotenv

from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.account_service import AccountService
from app.services.transaction_service import TransactionService
from config import get_settings
from database import SQLDatabase

settings = get_settings()
load_dotenv()


class ServiceDIContainer(containers.DeclarativeContainer):
    """Service Dependency Injection Container."""

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=[
            '.routers.base',
            '.routers.accounts',
            '.routers.transactions',
            '.schemas.transaction_schemas',
        ]
    )
    # OPTIMIZE: Load all env vars on this config
    config.from_dict({'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI')})

    # Database
    sql_db = providers.Singleton(SQLDatabase, db_url=config.SQLALCHEMY_DATABASE_URI)

    # Repositories
    account_repository = providers.Factory(AccountRepository, session=sql_db.provided.session)
    transaction_repository = providers.Factory(TransactionRepository, session=sql_db.provided.session)

    # Services
    account_service = providers.Factory(
        AccountService, session=sql_db.provided.session, account_repository=account_repository
    )
    transaction_service = providers.Factory(
        TransactionService, session=sql_db.provided.session, transaction_repository=transaction_repository
    )
