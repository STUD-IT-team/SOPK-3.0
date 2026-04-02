from .base import BaseModel, BaseModelRepository
from sqlmodel import Field, SQLModel
from enum import Enum
from abc import ABC
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import List
from uuid import UUID

import uuid

__all__ = ["Sex", "Department", "Activist", "ActivistRepository"]

class Sex(str, Enum):
    male = "male"
    female = "female"

class Department(str, Enum):
    smm = "smm"
    cod = "cod"
    smm_cod = "smm_cod"


class Activist(BaseModel, table=True):
    __tablename__ = "activists"

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

    Gender: Sex | None = Field(
        sa_column_kwargs={"name": "sex"}
    )

    Phone: PhoneNumber | None = Field(
        max_length=255,
        sa_column_kwargs={"name": "phone"}
    )

    PreferredDepartment: Department | None = Field(
        sa_column_kwargs={"name": "department"}
    )

    TimeslotID: UUID | None = Field(
        sa_column_kwargs={"name": "timeslotid"}
    )


class ActivistRepository(BaseModelRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Activist:
        raise NotImplementedError

    async def getUsername(self, username: str, for_update: bool = False) -> Activist:
        raise NotImplementedError
    
    async def save(self, model: Activist) -> Activist:
        raise NotImplementedError
    
    async def delete(self, id: uuid.UUID) -> None:
        raise NotImplementedError

    async def getAll(self, for_update: bool = False) -> List[Activist]:
        raise NotImplementedError
    
    
    
