from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime, Column, func
from datetime import datetime
import uuid


class BaseModel(SQLModel):
    ID: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"name": "id"}
    )

    CreatedAt: datetime = Field(
        default_factory=datetime.now,
         sa_column_kwargs={
            "name": "created_at",
            "server_default": func.now(),
        },
    )

    UpdatedAt: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={
            "name": "updated_at",
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )