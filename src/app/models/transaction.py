from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.account import Account
from app.models.core import TimestampedModel


class Transaction(TimestampedModel, table=True):
    __tablename__ = 'transactions'

    account_id: UUID = Field(foreign_key='accounts.id')
    account: 'Account' = Relationship(back_populates='transactions')

    amount: float
