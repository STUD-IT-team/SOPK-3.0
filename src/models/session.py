from .base import BaseModel, BaseModelRepository
from sqlmodel import Field, Relationship
from typing import List, Optional
from datetime import datetime
from abc import ABC
import uuid



class SessionActivist(BaseModel, table=True):
    __tablename__ = "sessions_activists"

    SessionId: uuid.UUID = Field(
        foreign_key="sessions.id",
        sa_column_kwargs={"name": "sessionid"}
    )

    ActivistId: uuid.UUID = Field(
        foreign_key="activists.id",
        sa_column_kwargs={"name": "activistid"}
    )

    Session: Optional["Session"] = Relationship(back_populates="Activists")


class SessionOrganizer(BaseModel, table=True):
    __tablename__ = "sessions_organizers"

    SessionId: uuid.UUID = Field(
        foreign_key="sessions.id",
        sa_column_kwargs={"name": "sessionid"}
    )

    OrganizerId: uuid.UUID = Field(
        foreign_key="organizers.id",
        sa_column_kwargs={"name": "organizerid"}
    )

    Session: Optional["Session"] = Relationship(back_populates="Organizers")


class Assessment(BaseModel, table=True):
    __tablename__ = "assessments"

    ActivistId: uuid.UUID = Field(
        foreign_key="activists.id",
        sa_column_kwargs={"name": "activistid"}
    )

    OrganizerId: uuid.UUID = Field(
        foreign_key="organizers.id",
        sa_column_kwargs={"name": "organizerid"}
    )

    SessionId: uuid.UUID = Field(
        foreign_key="sessions.id",
        sa_column_kwargs={"name": "sessionid"}
    )

    Logic: int = Field(
        ge=1,
        le=5,
        sa_column_kwargs={"name": "logic"}
    )

    Charm: int = Field(
        ge=1,
        le=5,
        sa_column_kwargs={"name": "charm"}
    )

    Speech: int = Field(
        ge=1,
        le=5,
        sa_column_kwargs={"name": "speech"}
    )

    Resourcefulness: int = Field(
        ge=1,
        le=5,
        sa_column_kwargs={"name": "resourcefulness"}
    )

    StressResilience: int = Field(
        ge=1,
        le=5,
        sa_column_kwargs={"name": "stressresilience"}
    )

    Worthy: bool = Field(
        sa_column_kwargs={"name": "worthy"}
    )

    Comment: str = Field(
        sa_column_kwargs={"name": "comment"}
    )

    Session: Optional["Session"] = Relationship(back_populates="Assessments")


class Session(BaseModel, table=True):
    __tablename__ = "sessions"

    JoinNumber: int = Field(
        ge=0,
        sa_column_kwargs={"name": "join_number"}
    )

    StartTime: datetime = Field(
        sa_column_kwargs={"name": "startt"}
    )

    EndTime: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"name": "endt"}
    )

    CreatedById: uuid.UUID = Field(
        foreign_key="organizers.id",
        sa_column_kwargs={"name": "created_by"}
    )

    Organizers: List[SessionOrganizer] = Relationship(back_populates="Session")
    Activists: List[SessionActivist] = Relationship(back_populates="Session")

    Assessments: List[Assessment] = Relationship(back_populates="Session")

class SessionRepository(BaseModelRepository):
    async def get(self, id: uuid.UUID, for_update: bool = False) -> Session:
        raise NotImplementedError

    async def getAll(self, for_update: bool = False) -> List[Session]:
        raise NotImplementedError

    async def save(self, model: Session) -> Session:
        raise NotImplementedError
    
    async def delete(self, id: uuid.UUID) -> None: 
        raise NotImplementedError
    