from .base import BaseModel
from sqlmodel import Field, SQLModel
from enum import Enum
from abc import ABC
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

    FullName: str = Field(
        max_length=255,
        sa_column_kwargs={"name": "full_name"}
    )

    IsAdmin: bool = Field(
        sa_column_kwargs={"name": "is_admin"}
    )

class OrganizerRepository(ABC):
    async def get(self, id: uuid.UUID) -> Organizer:
        raise NotImplementedError

    async def getUsername(self, username: str) -> Organizer:
        raise NotImplementedError
    
    async def save(self, model: BaseOrganizer) -> Organizer:
        raise NotImplementedError
    
    async def delete(self, id: uuid.UUID) -> None:
        raise NotImplementedError

    async def getAll(self) -> List[Organizer]:
        raise NotImplementedError