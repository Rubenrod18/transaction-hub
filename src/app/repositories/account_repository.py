from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.orm import Session

from app.models import Account
from app.repositories import core


class AccountRepository(
    core.FindByIdMixin,
    core.GetMixin,
):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        super().__init__(model=Account, session=session)
