import uuid
from datetime import datetime, timedelta
from operator import ge, le

import pytest

from app.models import Account
from app.services.account_service import AccountService
from database import session
from tests.common.base_tests.test_base_integration import TestBaseIntegration
from tests.common.factories.account_factory import AccountFactory


class _TestBaseAccountService(TestBaseIntegration):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.account_service = AccountService(session)


class TestFindByIdAccountService(_TestBaseAccountService):
    def test_find_account_found(self):
        account = AccountFactory()

        found_account = self.account_service.find_by_id(account.id)

        assert isinstance(found_account, Account)
        assert found_account.id == account.id

    def test_find_account_not_found(self):
        account_id = uuid.uuid4()

        found_account = self.account_service.find_by_id(account_id)

        assert found_account is None


class TestGetAccountService(_TestBaseAccountService):
    def test_get_accounts_found(self):
        [AccountFactory() for _ in range(2)]

        accounts = self.account_service.get()

        assert accounts
        assert len(accounts) == 2

    @pytest.mark.parametrize(
        'filters, total_expected_accounts',
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
    def test_get_accounts_found_filter_by_page_number(self, filters, total_expected_accounts):
        [AccountFactory() for _ in range(3)]

        accounts = self.account_service.get(**filters)

        assert len(accounts) == total_expected_accounts

    @pytest.mark.parametrize(
        'filters, total_expected_accounts',
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
    def test_get_accounts_found_filter_by_items_per_page(self, filters, total_expected_accounts):
        [AccountFactory() for _ in range(3)]

        accounts = self.account_service.get(**filters)

        assert len(accounts) == total_expected_accounts

    @pytest.mark.parametrize(
        'filters, comparator',
        [
            (
                {'order': [Account.created_at.asc()]},
                le,
            ),
            (
                {'order': [Account.created_at.desc()]},
                ge,
            ),
        ],
        ids=['asc', 'desc'],
    )
    def test_get_accounts_found_filter_by_order(self, filters, comparator):
        current_datetime = datetime.now()
        AccountFactory(created_at=current_datetime - timedelta(days=1))
        AccountFactory(created_at=current_datetime - timedelta(days=2))
        AccountFactory(created_at=current_datetime - timedelta(days=3))

        accounts = self.account_service.get(**filters)

        created_ats = [account.created_at for account in accounts]
        str_comparator = '<=' if comparator is le else '>='
        for prev, curr in zip(created_ats, created_ats[1:]):
            assert comparator(prev, curr), f'Sorting failed: {prev} {str_comparator} {curr}'
