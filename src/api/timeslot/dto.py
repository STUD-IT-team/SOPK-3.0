from pydantic import BaseModel as PydanticBaseModel
from typing import List
from uuid import UUID
from datetime import datetime


class TimeslotResponse(PydanticBaseModel):
    id: UUID
    start_time: datetime
    end_time: datetime
    slot_count: int


class AllTimeslotResponse(PydanticBaseModel):
    timeslots: List[TimeslotResponse]


class CreateTimeslotDto(PydanticBaseModel):
    start_time: datetime
    end_time: datetime
    slot_count: int
