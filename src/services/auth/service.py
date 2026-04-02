from typing import Tuple
from uuid import UUID

from  models import ActivistRepository, OrganizerRepository, Activist, Organizer
from models.common.uow import UnitOfWork
from .coder import AuthCredentialsEncoder, DecodeSecurityError
from .password import AuthInfoValidationService
from .hasher import PasswordHasher
from .dto import LoginDto, RegisterDto, MeResponse, AuthUser, AuthRole

__all__ = ["AuthService", "UsernameTakenError", "UsernameNotFound", "UserIDNotFound", "IncorrectPasswordError", "IncorrectCredentialsError", "AuthValidationError"]


class AuthService:
    def __init__(self,
                 uow: UnitOfWork,
                 hasher: PasswordHasher,
                 encoder: AuthCredentialsEncoder,
                 validator: AuthInfoValidationService
    ):
        self.hasher = hasher
        self.encoder = encoder
        self.validator = validator
        self.uow = uow


    async def Login(self, dto: LoginDto) -> str:
        try:
            self.validator.ValidateUsername(dto.username)
        except Exception as e:
            raise AuthValidationError(e)

        user, role = await self._get_by_username(dto.username)
        if user is None or role is None:
            raise UsernameNotFound(f"Username {dto.username} not found")

        if not self.hasher.HashAndCompare(dto.password, user.PasswordHash):
            raise IncorrectPasswordError("Passwords do not match")

        return self.encoder.Encode(user.ID)

    async def Register(self, dto: RegisterDto) -> AuthUser:
        try:
            self.validator.Validate(dto.username, dto.password)
        except Exception as e:
            raise AuthValidationError(e)

        user, role = await self._get_by_username(dto.username)
        if user is not None:
            raise UsernameTakenError(f'Username {dto.username} already taken')

        hashed = self.hasher.HashPassword(dto.password)

        activist = Activist(
            UserName=dto.username,
            PasswordHash=hashed,
        )

        async with self.uow as uow:
            rep = uow.get(ActivistRepository)
            await rep.save(activist)
            await uow.commit()

        return AuthUser(
            UserID=activist.ID,
            Username=dto.username,
            Role=AuthRole.Activist
        )

    async def Auth(self, credentials: str) -> AuthUser:
        try:
            user_id = self.encoder.Decode(credentials)
        except DecodeSecurityError as e:
            raise IncorrectCredentialsError(e)

        user, role = await self._get_by_id(user_id)
        if user is None or role is None:
            raise UserIDNotFound(f"{user_id} not found")

        return AuthUser(
            UserID=user.ID,
            Username=user.UserName,
            Role=role
        )

    async def Me(self, auser: AuthUser) -> MeResponse:
        user, role = await self._get_by_id(auser.UserID)
        if user is None or role is None:
            raise UserIDNotFound(f"{auser.UserID} not found")

        if role == AuthRole.Activist:
            return MeResponse(
                user_id=user.ID,
                username=user.UserName,
                full_name=user.FullName,
                gender=user.Gender,
                phone=user.Phone,
                preferred_department=user.PreferredDepartment,
                role=role
            )
        else:
            return MeResponse(
                user_id=user.ID,
                username=user.UserName,
                full_name=user.FullName,
                gender=None,
                phone=None,
                preferred_department=None,
                role=role
            )

    async def _get_by_username(self, username: str) -> Tuple[Activist | Organizer | None, AuthRole | None]:
        async with self.uow as uow:
            activist = await uow.get(ActivistRepository).getUsername(username)
            organizer = await uow.get(OrganizerRepository).getUsername(username)

        return self._define_role(activist, organizer)

    async def _get_by_id(self, id: UUID) -> Tuple[Activist | Organizer | None, AuthRole | None]:
        async with self.uow as uow:
            activist = await uow.get(ActivistRepository).get(id)
            organizer = await uow.get(OrganizerRepository).get(id)

        return self._define_role(activist, organizer)


    @staticmethod
    def _define_role(activist, organizer) -> Tuple[Activist | Organizer | None, AuthRole | None]:
        if organizer is not None:
            if organizer.IsAdmin:
                return organizer, AuthRole.Admin
            else:
                return organizer, AuthRole.Organizer
        elif activist is not None:
            return activist, AuthRole.Activist

        return None, None



class UsernameTakenError(Exception):
    pass

class UsernameNotFound(Exception):
    pass

class UserIDNotFound(Exception):
    pass

class IncorrectPasswordError(Exception):
    pass

class IncorrectCredentialsError(Exception):
    pass

class AuthValidationError(Exception):
    pass





