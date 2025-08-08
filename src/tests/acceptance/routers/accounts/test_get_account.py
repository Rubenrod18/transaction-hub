from app.utils.constants import DEFAULT_DATETIME_FORMAT
from tests.acceptance.routers.accounts._test_base_account import _TestBaseAccountEndpoints
from tests.common.factories.account_factory import AccountFactory


class TestGetAccountRouter(_TestBaseAccountEndpoints):
    def test_get_account(self):
        account = AccountFactory(deleted_at=None)
        response = self.client.get(url=f'{self.base_path}/{account.id}')
        json_response = response.json()

        assert json_response
        assert json_response['account_id'] == str(account.id)
        assert json_response['balance'] == account.balance
        assert json_response['created_at'] == account.created_at.strftime(DEFAULT_DATETIME_FORMAT)
        assert json_response['updated_at'] == account.updated_at.strftime(DEFAULT_DATETIME_FORMAT)
        assert json_response['deleted_at'] is None
