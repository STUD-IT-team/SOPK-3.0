import datetime
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel
from typing import List

from models import Sex, Department

class ActivistResponse(PydanticBaseModel):
    id: UUID
    username: str
    full_name: str | None
    sex: Sex | None
    department: Department | None
    phone: str | None
    timeslot_id: UUID | None

class AllActivistResponse(PydanticBaseModel):
    activists: List[ActivistResponse]

class UpdateActivistDataDto(PydanticBaseModel):
    full_name: str
    sex: Sex
    department: Department
    phone: str

class UpdateActivistTimeslotDto(PydanticBaseModel):
    timeslot_id: UUID

class ActivistSessionResponse(PydanticBaseModel):
    session_id: str
    join_number: int
    start_time: datetime | None


