from sqlmodel import Session

from app.repositories.account_repository import AccountRepository
from app.services import core


class AccountService(
    core.FindByIdMixin,
    core.GetMixin,
):
    def __init__(self, session: type[Session] = None, account_repository: AccountRepository = None):
        super().__init__(repository=account_repository or AccountRepository(session))
