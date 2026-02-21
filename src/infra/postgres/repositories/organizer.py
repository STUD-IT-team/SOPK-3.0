from .base import BaseRepository
from models import BaseOrganizerRepository, BaseOrganizer
from sqlmodel import select

import uuid

__all__ = ["BaseOrganizerPostgresRepository"]

class BaseOrganizerPostgresRepository(BaseRepository, BaseOrganizerRepository):    
    async def save(self, model: BaseOrganizer) -> BaseOrganizer:
        async with self._db.get_session() as session:
            session.add(model)
            await session.commit()
            return model
    
    async def get(self, id: uuid.UUID) -> BaseOrganizer:
        async with self._db.get_session() as session:
            return await session.get(BaseOrganizer, id)
    
    async def gettgid(self, tgid: int) -> BaseOrganizer:
        async with self._db.get_session() as session:
            query = select(BaseOrganizer).where(BaseOrganizer.TgID == tgid).limit(1)
            return await session.exec(query).first()