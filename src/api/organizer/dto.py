from pydantic import BaseModel as PydanticBaseModel
from typing import List
from uuid import UUID


class OrganizerResponse(PydanticBaseModel):
    id: UUID
    username: str
    full_name: str | None
    is_admin: bool


class AllOrganizerResponse(PydanticBaseModel):
    organizers: List[OrganizerResponse]


class CreateOrganizerDto(PydanticBaseModel):
    username: str
    password: str
    full_name: str | None


class UpdateOrganizerDataDto(PydanticBaseModel):
    full_name: str
