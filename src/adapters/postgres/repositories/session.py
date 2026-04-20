from sqlmodel import select, delete
from models import Session, SessionRepository
from .base import BaseRepository


class SqlAlchemySessionRepository(BaseRepository, SessionRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Session | None:
        query = select(Session).where(Session.ID == id)
        if for_update:
            query = query.with_for_update()
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def getByJoinNumber(self, join_number: int, for_update: bool = False) -> Session | None:
        query = select(Session).where(Session.JoinNumber == join_number)
        if for_update:
            query = query.with_for_update()
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def  getAll(self, for_update: bool = False) -> list[Session]:
        query = select(Session)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(query)
        return result.scalars().all()

    async def save(self, model: Session) -> Session:
        self.session.add(model)
        return model
    
    async def delete(self, id: uuid.UUID) -> None:
        query = delete(Session).where(Session.ID == id)
        await self.session.execute(query)
