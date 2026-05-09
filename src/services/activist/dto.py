from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from models import Sex, Department

__all__ = ["UpdateDataDto"]


class UpdateDataDto(PydanticBaseModel):
    FullName: str = Field(alias='full_name')
    Gender: Sex = Field(alias='sex')
    PreferredDepartment: Department = Field(alias='department')
    Phone: str = Field(alias='phone')
    
    model_config = ConfigDict(
        populate_by_name=True,
    )
