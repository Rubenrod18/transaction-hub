from tests.common.factories.account_factory import AccountFactory
from tests.common.seeds import seed_actions
from tests.common.seeds.core import FactorySeeder


class Seeder(FactorySeeder):
    def __init__(self):
        super().__init__(name='AccountSeeder', priority=0, factory=AccountFactory)
        self._default_rows = 5

    @seed_actions
    def seed(self, rows: int = None) -> None:
        self.factory.create_batch(rows or self._default_rows)
