from models.common.uow import UnitOfWork
from models import Activist, ActivistRepository
from .dto import *

__all__ = ["ActivistService"]


class ActivistService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def getAll(self) -> list[Activist]:
        async with self.uow:
            return await self.uow.get(ActivistRepository).getAll()
        
