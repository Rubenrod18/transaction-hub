from uuid import UUID

from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError

from app.di_container import ServiceDIContainer
from app.repositories.account_repository import AccountRepository
from app.schemas.core import IdMixin, TimestampMixin


class TransactionSchema(BaseModel, IdMixin, TimestampMixin):
    id: UUID = Field(..., alias='transaction_id')
    account_id: UUID
    amount: float

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TransactionRequestSchema(BaseModel):
    account_id: UUID
    amount: float

    @field_validator('account_id')
    @classmethod
    @inject
    def validate_account_id(
        cls, account_id: int, account_repository: AccountRepository = Provide[ServiceDIContainer.account_repository]
    ) -> UUID:
        if not account_repository.find_by_id(account_id):
            raise PydanticCustomError('account_id_not_found', 'Account ID not found')

        return account_id
