import uuid
from datetime import datetime, timedelta
from operator import ge, le

import pytest

from app.models import Account, Transaction
from app.repositories.transaction_repository import TransactionRepository
from database import session
from tests.common.base_tests.test_base_integration import TestBaseIntegration
from tests.common.factories.transaction_factory import TransactionFactory


class _TestBaseTransactionRepository(TestBaseIntegration):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.transaction_repository = TransactionRepository(session)


class TestFindByIdTransactionRepository(_TestBaseTransactionRepository):
    def test_find_transaction_found(self):
        transaction = TransactionFactory()

        found_transaction = self.transaction_repository.find_by_id(transaction.id)

        assert isinstance(found_transaction, Transaction)
        assert found_transaction.id == transaction.id

    def test_find_transaction_not_found(self):
        transaction_id = uuid.uuid4()

        found_transaction = self.transaction_repository.find_by_id(transaction_id)

        assert found_transaction is None


class TestGetTransactionRepository(_TestBaseTransactionRepository):
    def test_get_transactions_found(self):
        [TransactionFactory() for _ in range(2)]

        transactions = self.transaction_repository.get()

        assert transactions
        assert len(transactions) == 2

    @pytest.mark.parametrize(
        'filters, total_expected_transactions',
        [
            (
                {'page_number': 1, 'items_per_page': 3},
                3,
            ),
            (
                {'page_number': 2, 'items_per_page': 3},
                0,
            ),
        ],
        ids=['page_1', 'page_2'],
    )
    def test_get_transactions_found_filter_by_page_number(self, filters, total_expected_transactions):
        [TransactionFactory() for _ in range(3)]

        transactions = self.transaction_repository.get(**filters)

        assert len(transactions) == total_expected_transactions

    @pytest.mark.parametrize(
        'filters, total_expected_transactions',
        [
            (
                {'page_number': 1, 'items_per_page': 1},
                1,
            ),
            (
                {'page_number': 4, 'items_per_page': 1},
                0,
            ),
        ],
        ids=['page_1', 'page_2'],
    )
    def test_get_transactions_found_filter_by_items_per_page(self, filters, total_expected_transactions):
        [TransactionFactory() for _ in range(3)]

        transactions = self.transaction_repository.get(**filters)

        assert len(transactions) == total_expected_transactions

    @pytest.mark.parametrize(
        'filters, comparator',
        [
            (
                {'order': [Transaction.created_at.asc()]},
                le,
            ),
            (
                {'order': [Transaction.created_at.desc()]},
                ge,
            ),
        ],
        ids=['asc', 'desc'],
    )
    def test_get_transactions_found_filter_by_order(self, filters, comparator):
        current_datetime = datetime.now()
        TransactionFactory(created_at=current_datetime - timedelta(days=1))
        TransactionFactory(created_at=current_datetime - timedelta(days=2))
        TransactionFactory(created_at=current_datetime - timedelta(days=3))

        transactions = self.transaction_repository.get(**filters)

        created_ats = [transaction.created_at for transaction in transactions]
        str_comparator = '<=' if comparator is le else '>='
        for prev, curr in zip(created_ats, created_ats[1:]):
            assert comparator(prev, curr), f'Sorting failed: {prev} {str_comparator} {curr}'


class TestCreateTransactionRepository(_TestBaseTransactionRepository):
    def test_create_transaction(self):
        transaction_data = TransactionFactory.build_dict(exclude={'created_at', 'updated_at', 'deleted_at'})

        new_transaction = self.transaction_repository.create(**transaction_data)

        assert isinstance(new_transaction, Transaction)
        assert new_transaction.amount == transaction_data['amount']
        assert isinstance(new_transaction.account, Account)
