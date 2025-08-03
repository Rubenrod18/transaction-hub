"""CLI module for managing custom commands of the application."""

import typer
from sqlalchemy import orm

from app.cli import CreateDatabaseCli, SeederCli
from database import settings, SQLDatabase

app = typer.Typer()


@app.command(name='create_db', help='Create database.')
def create_database() -> None:
    """Command line script for creating the database."""
    cli = CreateDatabaseCli(db_uri=settings.SYNC_DATABASE_URL)
    cli.run_command()


@app.command(name='seed', help='Fill database with fake data.')
def seeds() -> None:
    """Command line script for filling database with fake data."""
    sql_db = SQLDatabase(db_url=settings.SYNC_DATABASE_URL)
    scoped_session = orm.scoped_session(sql_db.sessionmaker)

    with scoped_session() as session:
        seeder_cli = SeederCli(session=session)
        seeder_cli.run_command()


if __name__ == '__main__':
    app()
