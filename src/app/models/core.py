import uuid
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class BaseMixin(SQLModel):
    __abstract__ = True
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampedModel(BaseMixin):
    __abstract__ = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={'server_default': func.now()},  # pylint: disable=not-callable
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={'server_default': func.now(), 'onupdate': func.now()},  # pylint: disable=not-callable
        nullable=False,
    )
    deleted_at: datetime = Field(nullable=True)
