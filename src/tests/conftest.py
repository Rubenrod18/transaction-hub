import os
import uuid

import pytest
import sqlalchemy as sa
from dotenv import find_dotenv, load_dotenv
from faker import Faker
from fastapi.testclient import TestClient

from app import create_app
from app.cli import CreateDatabaseCli
from app.models.core import BaseMixin
from database import session

faker = Faker()


def pytest_configure():
    """Load .env.test before running tests"""
    load_dotenv(find_dotenv('.env.test'), override=True)


@pytest.fixture(scope='function', autouse=True)
def setup_database():
    def create_new_sqlalchemy_session() -> tuple[str, sa.Engine]:
        test_db_uri = f'{os.environ["SQLALCHEMY_DATABASE_URI"]}_{uuid.uuid4().hex}'
        test_engine = sa.create_engine(test_db_uri)
        session.remove()
        session.configure(bind=test_engine)
        original_db_uri = os.environ['SQLALCHEMY_DATABASE_URI']
        os.environ['SQLALCHEMY_DATABASE_URI'] = test_db_uri
        return original_db_uri, test_engine

    def create_db(engine: sa.Engine):
        seeder_cli = CreateDatabaseCli(db_uri=os.environ['SQLALCHEMY_DATABASE_URI'])
        seeder_cli.run_command()

        with engine.begin() as conn:
            BaseMixin.metadata.create_all(conn)

    def drop_db(engine: sa.Engine):
        db_name_to_drop = os.environ['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)[1]
        neutral_engine_url = engine.url.set(database='postgres')
        neutral_engine = sa.create_engine(neutral_engine_url, echo=True)

        try:
            with neutral_engine.connect() as conn:
                conn.execution_options(isolation_level='AUTOCOMMIT')
                conn.execute(
                    sa.text(f"""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = '{db_name_to_drop}';
                """)
                )
                conn.execute(sa.text(f'DROP DATABASE IF EXISTS "{db_name_to_drop}"'))
                print(f"Database '{db_name_to_drop}' dropped successfully.")  # noqa
        finally:
            neutral_engine.dispose()

    db_uri, sa_engine = create_new_sqlalchemy_session()
    create_db(sa_engine)
    yield
    drop_db(sa_engine)
    os.environ['SQLALCHEMY_DATABASE_URI'] = db_uri


@pytest.fixture
def app(setup_database):
    app = create_app()
    app.container.config.from_dict({'SQLALCHEMY_DATABASE_URI': os.environ['SQLALCHEMY_DATABASE_URI']})
    return app


@pytest.fixture
def client(app):
    yield TestClient(app)
