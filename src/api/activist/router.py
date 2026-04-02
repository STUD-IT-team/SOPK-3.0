from fastapi import APIRouter, Depends, HTTPException, status

from dependency_injector.wiring import inject, Provide

from api.activist.dto import ActivistResponse, AllActivistResponse, UpdateActivistDataDto, ActivistSessionResponse, \
    UpdateActivistTimeslotDto
from injection import Container

from uuid import UUID

from api import AuthCurrentUser, AuthRequireRole
from services.auth import AuthUser, AuthRole

router = APIRouter(prefix="/activist", tags=["Activist"])

@router.get(
    "/",
    response_model=AllActivistResponse,
    status_code=status.HTTP_200_OK,
    description="Get all activists",
)
@inject
def getAll(
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Organizer)),
):
    pass

@router.get(
    "/:id",
    response_model=ActivistResponse,
    status_code=status.HTTP_200_OK,
    description="Get an activist. Available to activist itself or organizer",
)
@inject
def getById(
        id: UUID,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Activist)),
):
    pass

@router.put(
    "/:id/data",
    status_code=status.HTTP_200_OK,
    response_model=ActivistResponse,
    description="Update an activist information (form). Available to activist itself only",
)
@inject
def updateData(
        id: UUID,
        data: UpdateActivistDataDto,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Activist)),
):
    pass

@router.put(
    "/:id/timeslot",
    status_code=status.HTTP_200_OK,
    response_model=ActivistResponse,
    description="Update (or firstly set) activist's timeslot. Available to activist itself or organizer",
)
@inject
def updateTimeslot(
        id: UUID,
        data: UpdateActivistTimeslotDto,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Activist)),
):
    pass

@router.delete(
    "/:id",
    status_code=status.HTTP_200_OK,
    description="Delete an activist. Available to admin only",
)
@inject
def delete(
        id: UUID,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Admin)),
):
    pass

@router.get(
    "/:id/session",
    response_model=ActivistSessionResponse | None,
    status_code=status.HTTP_200_OK,
    description="Get activist's session, if he's in one of them",
)
@inject
def getInSession(
        id: UUID,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Activist)),
):
    pass


@router.put(
    "/:id/join/:sessionId",
    response_model=ActivistSessionResponse,
    status_code=status.HTTP_200_OK,
    description="Join a session. Available to activist itself only",
)
@inject
def joinSession(
        id: UUID,
        sessionId: UUID,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Activist)),
):
    pass

