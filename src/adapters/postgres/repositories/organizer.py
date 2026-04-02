from sqlmodel import select

from models import Organizer, OrganizerRepository
from .base import BaseRepository

import uuid

class SqlAlchemyOrganizerRepository(BaseRepository, OrganizerRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Organizer | None:
        query = select(Organizer).where(Organizer.ID == id)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(
            query
        )
        return result.scalar_one_or_none()

    async def getUsername(self, username: str, for_update: bool = False) -> Organizer | None:
        query = select(Organizer).where(Organizer.UserName == username)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(
            query
        )
        return result.scalar_one_or_none()

    async def save(self, model: Organizer) -> Organizer:
        self.session.add(model)
        await self.session.flush()  # чтобы получить ID
        return model

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)

    async def getAll(self, for_update: bool = False):
        query = select(Organizer)
        if for_update:
            query = query.with_for_update()
        result = await self.session.execute(query)
        return result.scalars().all()