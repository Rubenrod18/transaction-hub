import random

from sqlalchemy import func

from app.models import Account
from app.repositories.account_repository import AccountRepository
from tests.common.factories.transaction_factory import TransactionFactory
from tests.common.seeds import seed_actions
from tests.common.seeds.core import FactorySeeder, RepositorySeeder
from tests.conftest import session


class Seeder(FactorySeeder, RepositorySeeder):
    def __init__(self):
        FactorySeeder.__init__(self, name='TransactionSeeder', priority=1, factory=TransactionFactory)
        RepositorySeeder.__init__(self, AccountRepository(session))
        self._default_rows = 30

    @staticmethod
    def _random_account() -> Account:
        return (
            session.query(Account)
            .order_by(func.random())  # pylint: disable=not-callable
            .limit(1)
            .one_or_none()
        )

    @seed_actions
    def seed(self, rows: int = None) -> None:
        rows = rows or self._default_rows

        for _ in range(rows):
            if random.choice([True, False]):
                self.factory.create(account_id=self._random_account())
            else:
                self.factory.create()
