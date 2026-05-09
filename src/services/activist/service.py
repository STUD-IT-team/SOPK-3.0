from uuid import UUID
from models import UnitOfWork
from models import Activist, ActivistRepository, TimeslotRepository
from .dto import UpdateDataDto

__all__ = [
    "ActivistService", "ActivistServiceError", "ActivistNotFoundError", "TimeslotNotFoundError", 
    "TimeslotAlreadyFullError"
    ]


class ActivistService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def getAll(self) -> list[Activist]:
        async with self.uow:
            return await self.uow.get(ActivistRepository).getAll()
        
    async def getById(self, id: UUID) -> Activist:
        async with self.uow:
            return await self._getActivistOrRaise(id)
    
    async def updateData(self, id: UUID, data: UpdateDataDto) -> Activist:
        async with self.uow:
            activist = await self._getActivistOrRaise(id, for_update=True)
            activist.sqlmodel_update(data)

        return activist
    
    async def delete(self, id: UUID) -> None:
        async with self.uow:
            await self.uow.get(ActivistRepository).delete(id)
            
    async def updateTimeslot(self, activistId: UUID, timeslotId: UUID) -> Activist:
        async with self.uow:
            tsRepo = self.uow.get(TimeslotRepository)
            ts = await tsRepo.get(timeslotId, for_update=True)  # timeslot acts as a mutex here
            if ts is None:
                raise TimeslotNotFoundError(f"Timeslot with id {timeslotId} not found")
            
            
            filledSlotsCount = await tsRepo.getFilledSlotsCount(ts)
            if filledSlotsCount >= ts.SlotCount:
                raise TimeslotAlreadyFullError(f"Timeslot with id {timeslotId} is already full")
            
            activist = await self._getActivistOrRaise(activistId, for_update=True)
            activist.TimeslotID = timeslotId
            
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

class TimeslotNotFoundError(ActivistServiceError):
    pass

class TimeslotAlreadyFullError(ActivistServiceError):
    pass
