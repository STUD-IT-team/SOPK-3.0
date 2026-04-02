from fastapi import APIRouter, Depends, HTTPException, status

from dependency_injector.wiring import inject, Provide
from injection import Container

from uuid import UUID

from api import AuthCurrentUser, AuthRequireRole
from services.auth import AuthUser, AuthRole

from .dto import (
    OrganizerResponse,
    AllOrganizerResponse,
    CreateOrganizerDto,
    UpdateOrganizerDataDto,
)

router = APIRouter(prefix="/organizer", tags=["Organizer"])


@router.get(
    "/",
    description="Get all organizers. Available to organizer or Admin",
    status_code=status.HTTP_200_OK,
    response_model=AllOrganizerResponse,
)
@inject
def getAll(
    user: AuthUser = Depends(AuthRequireRole(AuthRole.Organizer))
):
    pass


@router.get(
    "/:id",
    description="Get organizer by ID. Available to organizer or Admin",
    status_code=status.HTTP_200_OK,
    response_model=OrganizerResponse,
)
@inject
def getById(
        id: UUID,
        user: AuthUser = Depends(AuthRequireRole(AuthRole.Organizer)),
):
    pass


@router.post(
    "/",
    description="Create a new organizer. Available to Admin",
    status_code=status.HTTP_201_CREATED,
    response_model=OrganizerResponse,
)
@inject
def post(
    data: CreateOrganizerDto,
    user: AuthUser = Depends(AuthRequireRole(AuthRole.Admin)),
):
    pass


@router.put(
    "/:id/data",
    description="Update organizer data. Available to organizer itself or Admin",
    status_code=status.HTTP_200_OK,
    response_model=OrganizerResponse,
)
@inject
def updateData(
    id: UUID,
    data: UpdateOrganizerDataDto,
    user: AuthUser = Depends(AuthRequireRole(AuthRole.Organizer)),
):
    pass


@router.delete(
    "/:id", description="Delete organizer by ID. Available to organizer itself or Admin", status_code=status.HTTP_200_OK
)
@inject
def delete(
    id: UUID,
    user: AuthUser = Depends(AuthRequireRole(AuthRole.Organizer)),
):
    pass


@router.put(
    ":id/join/:sessionId",
    description="Organizer joins a session. Available to organizer itself or Admin",
    status_code=status.HTTP_200_OK,
    response_model=OrganizerResponse,
)
@inject
def joinSession(
    id: UUID,
    sessionId: UUID,
    user: AuthUser = Depends(AuthRequireRole(AuthRole.Organizer))
):
    pass
