from datetime import datetime
from uuid import UUID

import pytest

from app.models import Account, Transaction
from database import session
from tests.common.base_tests.test_base_integration import TestBaseIntegration
from tests.common.factories.transaction_factory import TransactionFactory
from tests.conftest import faker


class TestAccountModel(TestBaseIntegration):
    @pytest.mark.parametrize(
        'transaction_factory',
        [
            [TransactionFactory, TransactionFactory],
            TransactionFactory,
            None,
        ],
        ids=['several_transactions', 'one_transaction', 'no_transactions'],
    )
    def test_create_account(self, transaction_factory):
        account_data = {'balance': faker.pyfloat()}

        if isinstance(transaction_factory, list):
            account_data.update({'transactions': [factory() for factory in transaction_factory]})
        elif transaction_factory:
            account_data.update({'transactions': [transaction_factory()]})

        account = Account(deleted_at=None, **account_data)
        session.add(account)
        session.flush()
        session.commit()

        assert isinstance(account.id, UUID)
        assert isinstance(account.balance, float)
        assert isinstance(account.account_id, UUID)
        assert isinstance(account.created_at, datetime)
        assert isinstance(account.updated_at, datetime)
        assert account.deleted_at is None

        if isinstance(transaction_factory, list):
            assert account.transactions
            assert isinstance(account.transactions[0], Transaction)
            assert account.transactions[0] == account_data['transactions'][0]
            assert isinstance(account.transactions[1], Transaction)
            assert account.transactions[1] == account_data['transactions'][1]
        elif transaction_factory:
            assert account.transactions
            assert isinstance(account.transactions[0], Transaction)
            assert account.transactions[0] == account_data['transactions'][0]
        else:
            assert not account.transactions
