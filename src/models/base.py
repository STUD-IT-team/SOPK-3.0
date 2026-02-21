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
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), name="created_at"
        )
    )

    UpdatedAt: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), name="updated_at"
        )
    )