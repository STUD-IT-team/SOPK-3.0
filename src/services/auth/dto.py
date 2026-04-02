from pydantic import BaseModel as PydanticBaseModel
from uuid import UUID
from enum import Enum

__all__ = ["AuthUser", "AuthRole", "LoginDto", "RegisterDto", "MeResponse"]

from pydantic_extra_types.phone_numbers import PhoneNumber

from models import Department


class AuthRole(str, Enum):
    Activist = 'activist'
    Organizer = 'organizer'
    Admin = 'admin'


class AuthUser(PydanticBaseModel):
    UserID: UUID
    Username: str
    Role: AuthRole


class LoginDto(PydanticBaseModel):
    username: str
    password: str

class RegisterDto(PydanticBaseModel):
    username: str
    password: str

class MeResponse(PydanticBaseModel):
    user_id: UUID
    username: str
    role: AuthRole
    full_name: str | None
    gender: str | None
    phone: PhoneNumber | None
    preferred_department: Department | None

