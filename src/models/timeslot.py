from .base import BaseModel, BaseModelRepository
from sqlmodel import Field, SQLModel
from abc import ABC
import uuid
from  datetime import datetime
from typing import List

__all__ = ["Timeslot", "TimeslotRepository", "TimeslotAlreadyBusy", "TimeslotNotFound", "TimeslotNotAvailable"]

class Timeslot(BaseModel, table=True):
    __tablename__ = "timeslots"

    StartTime: datetime = Field(
        sa_column_kwargs={"name": "startt"}
    )

    EndTime: datetime = Field(
        sa_column_kwargs={"name": "endt"}
    )

    SlotCount: int = Field(
        default=0,
        ge=0,
        sa_column_kwargs={"name": "slotcnt"}
    )

class TimeslotRepository(BaseModelRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Timeslot:
        raise NotImplementedError

    async def getAll(self, for_update: bool = False) -> List[Timeslot]:
        raise NotImplementedError

    async def save(self, model: Timeslot) -> Timeslot:
        raise NotImplementedError
    
    async def saveBatch(self, models: List[Timeslot]) -> List[Timeslot]:
        raise NotImplementedError
    
    async def delete(self, id: uuid.UUID) -> None: 
        raise NotImplementedError
    
    async def deleteBatch(self, ids: List[uuid.UUID]) -> None:
        raise NotImplementedError

class TimeslotAlreadyBusy(Exception):
    pass

class TimeslotNotFound(Exception):
    pass

class TimeslotNotAvailable(Exception):
    pass