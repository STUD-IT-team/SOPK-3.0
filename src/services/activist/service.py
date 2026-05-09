from uuid import UUID
from models import UnitOfWork
from models import Activist, ActivistRepository
from .dto import UpdateDataDto

__all__ = ["ActivistService", "ActivistServiceError", "ActivistNotFoundError"]


class ActivistService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def getAll(self) -> list[Activist]:
        async with self.uow:
            return await self.uow.get(ActivistRepository).getAll()
        
    async def getById(self, id: UUID) -> Activist:
        async with self.uow:
            return await self._getActivistOrRaise(id)
    
    async def updateData(self, id: UUID, data: UpdateDataDto):
        async with self.uow:
            activist = await self._getActivistOrRaise(id, for_update=True)
            activist.sqlmodel_update(data)

        return activist
    
    async def _getActivistOrRaise(self, id: UUID, for_update: bool = False):
        activist = await self.uow.get(ActivistRepository).get(id, for_update=for_update)
        if activist is None:
            raise ActivistNotFoundError(f"Activist with id {id} not found")
        
        return activist
    

class ActivistServiceError(Exception):
    pass

class ActivistNotFoundError(ActivistServiceError):
    pass
