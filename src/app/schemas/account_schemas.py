from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.core import IdMixin, TimestampMixin


class AccountSchema(BaseModel, IdMixin, TimestampMixin):
    id: UUID = Field(..., alias='account_id')
    balance: float

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
