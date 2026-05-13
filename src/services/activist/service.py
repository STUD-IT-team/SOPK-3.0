from uuid import UUID
from models import UnitOfWork
from models import Activist, ActivistRepository, TimeslotRepository, Session, SessionRepository, SessionActivist
from .dto import UpdateDataDto

__all__ = [
    "ActivistService", "ActivistServiceError", "ActivistNotFoundError", "TimeslotNotFoundError", 
    "TimeslotAlreadyFullError", "SessionNotFoundError", "SessionAlreadyFinishedError", "AlreadyJoinedSessionError"
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
                raise TimeslotNotFoundError(timeslotId)
            
            
            filledSlotsCount = await tsRepo.getFilledSlotsCount(ts)
            if filledSlotsCount >= ts.SlotCount:
                raise TimeslotAlreadyFullError(timeslotId)
            
            activist = await self._getActivistOrRaise(activistId, for_update=True)
            activist.TimeslotID = timeslotId
            
        return activist
    
    async def getInSession(self, id: UUID) -> Session | None:
        async with self.uow:
            return await self._getActiveSession(id)
    
    async def joinSession(self, id: UUID, sessionId: UUID) -> Session:
        async with self.uow:
            activeSession = await self._getActiveSession(id)
            if activeSession is not None:
                raise AlreadyJoinedSessionError(id)
            
            session = await self._getSessionOrRaise(sessionId)
            if session.EndTime is not None:
                raise SessionAlreadyFinishedError(sessionId)

            sessionActivist = SessionActivist(ActivistId=id, SessionId=sessionId)
            await self.uow.get(SessionRepository).save(sessionActivist)
            
        return session
            
    async def _getActivistOrRaise(self, id: UUID, for_update: bool = False):
        activist = await self.uow.get(ActivistRepository).get(id, for_update=for_update)
        if activist is None:
            raise ActivistNotFoundError(id)
        
        return activist
    
    async def _getActiveSession(self, id: UUID, for_update: bool = False) -> Session | None:
        return await self.uow.get(ActivistRepository).getActiveSession(id, for_update=for_update)
    
    async def _getSessionOrRaise(self, id: UUID, for_update: bool = False) -> Session:
        session = await self.uow.get(SessionRepository).get(id, for_update=for_update)
        if session is None:
            raise SessionNotFoundError(id)
        
        return session

class ActivistServiceError(Exception):
    pass

class ActivistNotFoundError(ActivistServiceError):
    def __init__(self, id: UUID):
        super().__init__(f"Activist with id {id} not found")

class TimeslotNotFoundError(ActivistServiceError):
    def __init__(self, id: UUID):
        super().__init__(f"Timeslot with id {id} not found")

class TimeslotAlreadyFullError(ActivistServiceError):
    def __init__(self, id: UUID):
        super().__init__(f"Timeslot with id {id} is already full")

class SessionNotFoundError(ActivistServiceError):
    def __init__(self, id: UUID):
        super().__init__(f"Session with id {id} not found")

class SessionAlreadyFinishedError(ActivistServiceError):
    def __init__(self, id: UUID):
        super().__init__(f"Session with id {id} is already finished")

class AlreadyJoinedSessionError(ActivistServiceError):
    def __init__(self, id: UUID):
        super().__init__(f"Activist with id {id} is already in a session")
