from datetime import datetime, timedelta

import pytest

from app.utils.constants import DEFAULT_DATETIME_FORMAT
from tests.acceptance.routers.accounts._test_base_account import _TestBaseAccountEndpoints
from tests.common.factories.account_factory import AccountFactory


class TestListAccountRouter(_TestBaseAccountEndpoints):
    def test_list_accounts(self):
        current_dt = datetime.now()
        account = AccountFactory(created_at=current_dt - timedelta(days=1), deleted_at=None)
        account_2 = AccountFactory(created_at=current_dt, deleted_at=None)
        accounts = [account, account_2]

        response = self.client.get(url=self.base_path)
        json_response = response.json()

        assert json_response
        assert len(json_response) == len(accounts)

        for i, account in enumerate(json_response):
            assert account['account_id'] == str(accounts[i].id)
            assert account['balance'] == accounts[i].balance
            assert account['created_at'] == accounts[i].created_at.strftime(DEFAULT_DATETIME_FORMAT)
            assert account['updated_at'] == accounts[i].updated_at.strftime(DEFAULT_DATETIME_FORMAT)
            assert account['deleted_at'] is None

    @pytest.mark.parametrize(
        'page_number, items_per_page, total_expected_accounts',
        [
            (1, 3, 3),
            (2, 3, 0),
        ],
        ids=['page_1', 'page_2'],
    )
    def test_get_accounts_found_filter_by_page_number(self, page_number, items_per_page, total_expected_accounts):
        [AccountFactory() for _ in range(3)]
        query_params = f'page_number={page_number}&items_per_page={items_per_page}'

        response = self.client.get(url=f'{self.base_path}?{query_params}')
        json_response = response.json()

        assert len(json_response) == total_expected_accounts

    @pytest.mark.parametrize(
        'page_number, items_per_page, total_expected_accounts',
        [
            (1, 1, 1),
            (4, 1, 0),
        ],
        ids=['page_1', 'page_2'],
    )
    def test_get_accounts_found_filter_by_items_per_page(self, page_number, items_per_page, total_expected_accounts):
        [AccountFactory() for _ in range(3)]
        query_params = f'page_number={page_number}&items_per_page={items_per_page}'

        response = self.client.get(url=f'{self.base_path}?{query_params}')
        json_response = response.json()

        assert len(json_response) == total_expected_accounts
