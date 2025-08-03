from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.orm import Session

from app.models import Transaction
from app.repositories import core


class TransactionRepository(
    core.FindByIdMixin,
    core.GetMixin,
    core.CreateRepository,
):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        super().__init__(model=Transaction, session=session)

    def create(self, **kwargs) -> Transaction:
        with self.session() as session:
            transaction = self.model(**kwargs)
            session.add(transaction)
            session.flush()
            session.commit()
            return transaction
