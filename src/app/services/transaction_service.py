from sqlmodel import Session

from app.models import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.services import core


class TransactionService(
    core.FindByIdMixin,
    core.CreateService,
    core.GetMixin,
):
    def __init__(self, session: type[Session] = None, transaction_repository: TransactionRepository = None):
        super().__init__(repository=transaction_repository or TransactionRepository(session))

    def create(self, **kwargs) -> Transaction:
        return self.repository.create(**kwargs)
