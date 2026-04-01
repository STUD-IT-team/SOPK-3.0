from .base import BaseModel
from sqlmodel import Field, SQLModel
from abc import ABC
import uuid

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

class TimeslotRepository(ABC):
    async def get(self, id: uuid.UUID) -> Timeslot:
        raise NotImplementedError

    async def getAll(self) -> List[Timeslot]:
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