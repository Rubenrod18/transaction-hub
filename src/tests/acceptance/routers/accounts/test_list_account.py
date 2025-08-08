from datetime import datetime, timedelta

from app.utils.constants import DEFAULT_DATETIME_FORMAT
from tests.acceptance.routers.accounts._test_base_account import _TestBaseAccountEndpoints
from tests.common.factories.account_factory import AccountFactory


# TODO: Pending to define query_params in `get_account_list` endpoint.
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
