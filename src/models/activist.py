from .base import BaseModel
from sqlmodel import Field, SQLModel
from enum import Enum
from abc import ABC
from pydantic_extra_types.phone_numbers import PhoneNumber

import uuid

__all__ = ["Sex", "Department", "BaseActivist", "BaseActivistRepository"]

class Sex(str, Enum):
    male = "male"
    female = "female"

class Department(str, Enum):
    smm = "smm"
    cod = "cod"
    smm_cod = "smm_cod"


class BaseActivist(BaseModel, table=True):
    __tablename__ = "activists"

    TgID: int = Field(
        gt=0,
        sa_column_kwargs={"name": "tgid"}
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


class BaseActivistRepository(ABC):
    async def get(self, id: uuid.UUID) -> BaseActivist:
        raise NotImplementedError
    
    async def gettgid(self, tgid: int) -> BaseActivist:
        raise NotImplementedError
    
    async def save(self, model: BaseActivist) -> BaseActivist:
        raise NotImplementedError
    
    
    
