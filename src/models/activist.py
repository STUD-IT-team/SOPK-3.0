from .base import BaseModel
from sqlmodel import Field, SQLModel
from enum import Enum
from abc import ABC
from pydantic_extra_types.phone_numbers import PhoneNumber

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

    FullName: str = Field(
        max_length=255,
        sa_column_kwargs={"name": "full_name"}
    )

    Gender: Sex = Field(
        sa_column_kwargs={"name": "sex"}
    )

    Phone: PhoneNumber = Field(
        max_length=255,
        sa_column_kwargs={"name": "phone"}
    )

    PreferredDepartment: Department = Field(
        sa_column_kwargs={"name": "department"}
    )


class ActivistRepository(ABC):
    async def get(self, id: uuid.UUID) -> Activist:
        raise NotImplementedError

    async def getUsername(self, username: str) -> Activist:
        raise NotImplementedError
    
    async def save(self, model: BaseActivist) -> Activist:
        raise NotImplementedError
    
    async def delete(self, id: uuid.UUID) -> None:
        raise NotImplementedError

    async def getAll(self) -> List[Activist]:
        raise NotImplementedError
    
    
    
