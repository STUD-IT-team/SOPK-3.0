from sqlmodel import select

from models import Activist, ActivistRepository
from .base import BaseRepository

import uuid

class SqlAlchemyActivistRepository(BaseRepository, ActivistRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Activist | None:
        query = select(Activist).where(Activist.ID == id)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(
            query
        )
        return result.scalar_one_or_none()

    async def getUsername(self, username: str, for_update: bool = False) -> Activist | None:
        query = select(Activist).where(Activist.UserName == username)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(
            query
        )
        return result.scalar_one_or_none()

    async def save(self, model: Activist) -> Activist:
        self.session.add(model)
        return model

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)

    async def getAll(self, for_update: bool = False):
        query = select(Activist)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(query)
        return result.scalars().all()