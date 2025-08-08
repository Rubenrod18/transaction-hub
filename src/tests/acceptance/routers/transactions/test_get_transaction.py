from app.utils.constants import DEFAULT_DATETIME_FORMAT
from tests.acceptance.routers.transactions._test_base_transaction import _TestBaseTransactionEndpoints
from tests.common.factories.transaction_factory import TransactionFactory


class TestGetTransactionRouter(_TestBaseTransactionEndpoints):
    def test_get_transaction(self):
        transaction = TransactionFactory(deleted_at=None)

        response = self.client.get(url=f'{self.base_path}/{transaction.id}')
        json_response = response.json()

        assert json_response
        assert json_response['transaction_id'] == str(transaction.id)
        assert json_response['account_id'] == str(transaction.account_id)
        assert json_response['amount'] == transaction.amount
        assert json_response['created_at'] == transaction.created_at.strftime(DEFAULT_DATETIME_FORMAT)
        assert json_response['updated_at'] == transaction.updated_at.strftime(DEFAULT_DATETIME_FORMAT)
        assert json_response['deleted_at'] is None
