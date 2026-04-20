from uuid import UUID
from sqlmodel import select, delete, func
from models import Timeslot, TimeslotRepository, Activist
from .base import BaseRepository


class SqlAlchemyTimeslotRepository(BaseRepository, TimeslotRepository):
    async def get(self, id: UUID, for_update: bool = False) -> Timeslot | None:
        query = select(Timeslot).where(Timeslot.ID == id)
        if for_update:
            query = query.with_for_update()
            
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def getAll(self, for_update: bool = False) -> list[Timeslot]:
        query = select(Timeslot)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def getFilledSlotsCount(self, model: Timeslot) -> int:
        query = select(func.count()).select_from(Activist).where(Activist.TimeslotID == model.ID)
        count = await self.session.scalar(query)
        return count
        
    async def save(self, model: Timeslot) -> Timeslot:
        self.session.add(model)
        return model

    async def saveBatch(self, models: list[Timeslot]) -> list[Timeslot]:
        self.session.add_all(models)
        return models
    
    async def delete(self, id: UUID) -> None:
        query = delete(Timeslot).where(Timeslot.ID == id)
        await self.session.execute(query)
            
    async def deleteBatch(self, ids: list[UUID]) -> None:
        query = delete(Timeslot).where(Timeslot.ID.in_(ids))
        await self.session.execute(query)
    