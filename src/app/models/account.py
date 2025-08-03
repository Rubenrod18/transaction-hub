import typing as t
from uuid import UUID

from sqlmodel import Relationship

from app.models.core import TimestampedModel


class Account(TimestampedModel, table=True):
    __tablename__ = 'accounts'

    transactions: t.Optional['Transaction'] = Relationship(back_populates='account')

    balance: float

    @property
    def account_id(self) -> UUID:
        return self.id
