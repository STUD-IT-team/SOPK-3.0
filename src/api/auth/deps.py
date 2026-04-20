from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from dependency_injector.wiring import inject, Provide
from injection import Container

from services.auth import AuthService, IncorrectCredentialsError, UserIDNotFound
from services.auth import AuthUser, AuthRole

security = HTTPBearer()

__all__ = ["AuthCurrentUser", "AuthRequireRoles", "AuthRequireRolesOrUserItself", "OrganizerOrActivistItself"]

@inject
async def AuthCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(Provide[Container.authService])
) -> AuthUser:
    try:
        return await auth_service.Auth(credentials.credentials)

    except IncorrectCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    except UserIDNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

def AuthRequireRoles(*required_roles: AuthRole):
    async def role_checker(user: AuthUser = Depends(AuthCurrentUser)) -> AuthUser:
        if user.Role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user

    return role_checker


def AuthRequireRolesOrUserItself(*required_roles: AuthRole, owner_role: AuthRole):
    async def role_checker(
        id: UUID, 
        user: AuthUser = Depends(AuthRequireRoles(*required_roles, owner_role))
    ) -> AuthUser:
        if (user.Role == owner_role and user.UserID == id) or (user.Role in required_roles):
            return user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    return role_checker


OrganizerOrActivistItself = AuthRequireRolesOrUserItself(AuthRole.Organizer, owner_role=AuthRole.Activist)
