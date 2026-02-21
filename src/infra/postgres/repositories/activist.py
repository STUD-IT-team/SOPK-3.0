from .base import BaseRepository
from models import BaseActivistRepository, BaseActivist
from sqlmodel import select

import uuid

__all__ = ["BaseActivistPostgresRepository"]

class BaseActivistPostgresRepository(BaseRepository, BaseActivistRepository):    
    async def save(self, model: BaseActivist) -> BaseActivist:
        async with self._db.get_session() as session:
            session.add(model)
            await session.commit()
            return model
    
    async def get(self, id: uuid.UUID) -> BaseActivist:
        async with self._db.get_session() as session:
            return await session.get(BaseActivist, id)
    
    async def gettgid(self, tgid: int) -> BaseActivist:
        async with self._db.get_session() as session:
            query = select(BaseActivist).where(BaseActivist.TgID == tgid).limit(1)
            return await session.exec(query).first()
            

