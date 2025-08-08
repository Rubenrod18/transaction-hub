from datetime import datetime, timedelta

from app.utils.constants import DEFAULT_DATETIME_FORMAT
from tests.acceptance.routers.transactions._test_base_transaction import _TestBaseTransactionEndpoints
from tests.common.factories.transaction_factory import TransactionFactory


# TODO: Pending to define query_params in `get_account_list` endpoint.
class TestListTransactionRouter(_TestBaseTransactionEndpoints):
    def test_list_transactions(self):
        current_dt = datetime.now()
        transaction = TransactionFactory(created_at=current_dt - timedelta(days=1), deleted_at=None)
        transaction_2 = TransactionFactory(created_at=current_dt, deleted_at=None)
        transactions = [transaction, transaction_2]

        response = self.client.get(url=self.base_path)
        json_response = response.json()

        assert json_response
        assert len(json_response) == len(transactions)

        for i, transaction in enumerate(json_response):
            assert transaction['transaction_id'] == str(transactions[i].id)
            assert transaction['account_id'] == str(transactions[i].account_id)
            assert transaction['amount'] == transactions[i].amount
            assert transaction['created_at'] == transactions[i].created_at.strftime(DEFAULT_DATETIME_FORMAT)
            assert transaction['updated_at'] == transactions[i].updated_at.strftime(DEFAULT_DATETIME_FORMAT)
            assert transaction['deleted_at'] is None
