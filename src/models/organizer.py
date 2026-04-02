from .base import BaseModel, BaseModelRepository
from sqlmodel import Field, SQLModel
from abc import ABC
from typing import List
import uuid

__all__ = ["Organizer", "OrganizerRepository"]

class Organizer(BaseModel, table=True):
    __tablename__ = "organizers"

    UserName: str = Field(
        max_length=255,
        unique=True,
        sa_column_kwargs={"name": "username"}
    )

    PasswordHash: str = Field(
        sa_column_kwargs={"name": "password_hash"}
    )

    FullName: str | None = Field(
        max_length=255,
        sa_column_kwargs={"name": "full_name"}
    )

    IsAdmin: bool = Field(
        sa_column_kwargs={"name": "is_admin"},
        default=False
    )

class OrganizerRepository(BaseModelRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Organizer:
        raise NotImplementedError

    async def getUsername(self, username: str, for_update: bool = False) -> Organizer:
        raise NotImplementedError
    
    async def save(self, model: Organizer) -> Organizer:
        raise NotImplementedError
    
    async def delete(self, id: uuid.UUID) -> None:
        raise NotImplementedError

    async def getAll(self, for_update: bool = False) -> List[Organizer]:
        raise NotImplementedError