from pydantic import BaseModel as PydanticBaseModel
from typing import List
from uuid import UUID
from datetime import datetime

from models import Department, Sex


class ActivistInSessionResponse(PydanticBaseModel):
    id: UUID
    username: str
    full_name: str
    sex: Sex
    department: Department
    phone: str

class OrganizerInSessionResponse(PydanticBaseModel):
    id: UUID
    username: str
    full_name: str


class SessionResponse(PydanticBaseModel):
    id: UUID
    join_number: int
    start_time: datetime
    end_time: datetime | None
    created_by_id: OrganizerInSessionResponse
    organizers: List[OrganizerInSessionResponse]
    activists: List[ActivistInSessionResponse]


class AllSessionResponse(PydanticBaseModel):
    sessions: List[SessionResponse]


class AssessmentResponse(PydanticBaseModel):
    activist: ActivistInSessionResponse
    organizer_id: OrganizerInSessionResponse
    logic: int
    charm: int
    speech: int
    resourcefulness: int
    stress_resilience: int
    worthy: bool
    comment: str

class AllAssessmentResponse(PydanticBaseModel):
    assessments: List[AssessmentResponse]

class UpdateAssessmentDto(PydanticBaseModel):
    logic: int
    charm: int
    speech: int
    resourcefulness: int
    stress_resilience: int
    worthy: bool
    comment: str

class CanEndResponse:
    ok: bool
