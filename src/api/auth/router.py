from fastapi import APIRouter, Depends, HTTPException, status

from dependency_injector.wiring import inject, Provide
from injection import Container

from services.auth import AuthService, UsernameNotFound, IncorrectPasswordError, UsernameTakenError, AuthValidationError
from services.auth import LoginDto, RegisterDto, MeResponse, AuthUser

from .deps import AuthCurrentUser

__all__ = ["router"]

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
@inject
async def login(
    dto: LoginDto,
    auth_service: AuthService = Depends(Provide[Container.authService])
):
    try:
        token = await auth_service.Login(dto)
        return {"access_token": token, "token_type": "bearer"}

    except UsernameNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    except IncorrectPasswordError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

@router.post("/register")
@inject
async def register(
    dto: RegisterDto,
    auth_service: AuthService = Depends(Provide[Container.authService])
):
    try:
        await auth_service.Register(dto)

    except AuthValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except UsernameTakenError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )


@router.post("/logout")
async def logout(
    user: AuthUser = Depends(AuthCurrentUser)
):
    return {"access_token": "", "token_type": "none"}

@router.get("/me", response_model=MeResponse)
@inject
async def me(
    user: AuthUser = Depends(AuthCurrentUser),
    auth_service: AuthService = Depends(Provide[Container.authService])
):
    try:
        return await auth_service.Me(user)

    except UsernameNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

