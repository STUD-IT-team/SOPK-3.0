from abc import ABC, abstractmethod
from typing import Type, TypeVar
from models import BaseModelRepository


__all__ = ["UnitOfWork", "Repository"]

Repository = TypeVar('Repository', bound='BaseModelRepository')


class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> 'UnitOfWork':
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    def get(self, t: Type[Repository]) -> Repository:
        pass
