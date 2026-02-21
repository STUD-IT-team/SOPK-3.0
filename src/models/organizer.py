from .base import BaseModel
from sqlmodel import Field, SQLModel
from enum import Enum
from abc import ABC

import uuid

__all__ = ["BaseOrganizer", "BaseOrganizerRepository"]

class BaseOrganizer(BaseModel, table=True):
    __tablename__ = "organizers"

    TgID: int = Field(
        gt=0,
        sa_column_kwargs={"name": "tgid"}
    )

    TgNick: str = Field(
        max_length=255,
        sa_column_kwargs={"name": "tgnick"}
    )

    FullName: str = Field(
        max_length=255,
        sa_column_kwargs={"name": "full_name"}
    )

class BaseOrganizerRepository(ABC):
    async def get(self, id: uuid.UUID) -> BaseOrganizer:
        raise NotImplementedError
    
    async def gettgid(self, tgid: int) -> BaseOrganizer:
        raise NotImplementedError
    
    async def save(self, model: BaseOrganizer) -> BaseOrganizer:    
        raise NotImplementedError