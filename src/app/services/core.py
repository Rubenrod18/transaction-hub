from abc import ABC, abstractmethod
from typing import Any

from sqlmodel import SQLModel

from app.repositories.core import BaseRepository


class BaseService(ABC):
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository


class CreateService(ABC):
    @abstractmethod
    def create(self, **kwargs) -> SQLModel:
        raise NotImplementedError


class FindByIdService(ABC):
    @abstractmethod
    def find_by_id(self, record_id: Any) -> SQLModel:
        raise NotImplementedError


class GetService(ABC):
    @abstractmethod
    def get(self, **kwargs) -> list[SQLModel]:
        raise NotImplementedError


class FindByIdMixin(BaseService, FindByIdService):
    def find_by_id(self, record_id: Any) -> SQLModel | None:
        return self.repository.find_by_id(record_id)


class GetMixin(BaseService, GetService):
    def get(self, **kwargs) -> list[SQLModel]:
        return self.repository.get(**kwargs)
