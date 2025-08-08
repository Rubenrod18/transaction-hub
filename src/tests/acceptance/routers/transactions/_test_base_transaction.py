# pylint: disable=attribute-defined-outside-init, unused-argument
import pytest

from tests.common.base_tests.test_base_acceptance import TestBaseApi


class _TestBaseTransactionEndpoints(TestBaseApi):
    @pytest.fixture(autouse=True)
    def base_setup(self):
        self.base_path = f'{self.base_path}/transactions'
