from datetime import datetime
from uuid import UUID


class IdMixin:
    id: UUID


class TimestampMixin:
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
