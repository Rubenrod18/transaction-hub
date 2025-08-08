from uuid import UUID

from tests.acceptance.routers.transactions._test_base_transaction import _TestBaseTransactionEndpoints
from tests.common.factories.account_factory import AccountFactory


class TestCreateTransactionRouter(_TestBaseTransactionEndpoints):
    def test_create_transaction(self):
        account = AccountFactory(deleted_at=None)
        payload = {'account_id': str(account.id), 'amount': self.faker.pyfloat()}

        response = self.client.post(url=self.base_path, json=payload)
        json_response = response.json()

        assert json_response
        assert UUID(json_response['transaction_id'])
        assert json_response['account_id'] == str(account.id)
        assert json_response['amount'] == payload['amount']
        assert json_response['created_at']
        assert json_response['updated_at']
        assert json_response['deleted_at'] is None
