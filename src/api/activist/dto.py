import datetime
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from typing import List

from models import Sex, Department

class ActivistResponse(PydanticBaseModel):
    ID: UUID = Field(alias='id')
    UserName: str = Field(alias='username')
    FullName: str | None = Field(alias='full_name')
    Gender: Sex | None = Field(alias='sex')
    PreferredDepartment: Department | None = Field(alias='department')
    Phone: str | None = Field(alias='phone')
    TimeslotID: UUID | None = Field(alias='timeslot_id')
    
    model_config = ConfigDict(
        populate_by_name=True,
    )

class AllActivistResponse(PydanticBaseModel):
    activists: List[ActivistResponse]

class UpdateActivistDataDto(PydanticBaseModel):
    FullName: str = Field(alias='full_name')
    Gender: Sex = Field(alias='sex')
    PreferredDepartment: Department = Field(alias='department')
    Phone: str = Field(alias='phone')
    
    model_config = ConfigDict(
        populate_by_name=True,
    )

class UpdateActivistTimeslotDto(PydanticBaseModel):
    TimeslotID: UUID = Field(alias='timeslot_id')
    
    model_config = ConfigDict(
        populate_by_name=True,
    )

class ActivistSessionResponse(PydanticBaseModel):
    ID: UUID = Field(alias='session_id')
    JoinNumber: int = Field(alias='join_number')
    StartTime: datetime | None = Field(alias='start_time')
    
    model_config = ConfigDict(
        populate_by_name=True,
    )
