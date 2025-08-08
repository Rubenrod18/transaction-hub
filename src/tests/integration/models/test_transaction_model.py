from datetime import datetime
from uuid import UUID

from app.models import Account, Transaction
from database import session
from tests.common.base_tests.test_base_integration import TestBaseIntegration
from tests.common.factories.account_factory import AccountFactory


class TestTransactionModel(TestBaseIntegration):
    def test_create_transaction(self):
        account = AccountFactory(deleted_at=None)
        transaction_data = {'amount': self.faker.pyfloat(), 'account_id': account.id}

        transaction = Transaction(deleted_at=None, **transaction_data)
        session.add(transaction)
        session.flush()
        session.commit()

        assert isinstance(transaction.id, UUID)
        assert isinstance(transaction.amount, float)
        assert isinstance(transaction.account_id, UUID)
        assert isinstance(transaction.account, Account)
        assert transaction.account == account
        assert isinstance(transaction.created_at, datetime)
        assert isinstance(transaction.updated_at, datetime)
        assert transaction.deleted_at is None
