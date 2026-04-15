from fastapi import APIRouter, Depends, status, HTTPException

from dependency_injector.wiring import inject, Provide

from api.activist.dto import ActivistResponse, AllActivistResponse, UpdateActivistDataDto, ActivistSessionResponse, \
    UpdateActivistTimeslotDto
from injection import Container, UnitOfWork
from models import ActivistRepository

from uuid import UUID

from api import AuthRequireRoles, OrganizerOrActivistItself, AuthRequireRolesOrUserItself
from services.auth import AuthUser, AuthRole

router = APIRouter(prefix="/activist", tags=["Activist"])


@router.get(
    "/",
    response_model=AllActivistResponse,
    status_code=status.HTTP_200_OK,
    description="Get all activists",
    dependencies=[Depends(AuthRequireRoles(AuthRole.Organizer))]
)
@inject
async def getAll(uow: UnitOfWork = Depends(Provide[Container.uow])):
    async with uow as uow:
        activists = await uow.get(ActivistRepository).getAll()
    
    return {"activists": activists}


@router.get(
    "/{id}",
    dependencies=[Depends(OrganizerOrActivistItself)],
    response_model=ActivistResponse,
    status_code=status.HTTP_200_OK,
    description="Get an activist. Available to activist itself or organizer",
)
@inject
async def getById(
        id: UUID,
        uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow as uow:
        activist = await uow.get(ActivistRepository).get(id)
    
    return activist
        

@router.put(
    "/{id}/data",
    status_code=status.HTTP_200_OK,
    response_model=ActivistResponse,
    description="Update an activist information (form). Available to activist itself only",
)
@inject
async def updateData(
        data: UpdateActivistDataDto,
        user: AuthUser = Depends(AuthRequireRolesOrUserItself(owner_role=AuthRole.Activist)),
        uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    async with uow as uow:
        activist = await uow.get(ActivistRepository).get(user.UserID)
        activist.sqlmodel_update(data)
        
    return activist


@router.put(
    "/{id}/timeslot",
    status_code=status.HTTP_200_OK,
    response_model=ActivistResponse,
    description="Update (or firstly set) activist's timeslot. Available to activist itself or organizer",
)
@inject
def updateTimeslot(
        id: UUID,
        data: UpdateActivistTimeslotDto,
        user: AuthUser = Depends(AuthRequireRoles(AuthRole.Activist)),
):
    pass


@router.delete(
    "/{id}",
    dependencies=[Depends(AuthRequireRoles(AuthRole.Admin))],
    status_code=status.HTTP_200_OK,
    description="Delete an activist. Available to admin only",
)
@inject
async def delete(id: UUID, uow: UnitOfWork = Depends(Provide[Container.uow])):
    async with uow as uow:
        await uow.get(ActivistRepository).delete(id)


@router.get(
    "/{id}/session",
    response_model=ActivistSessionResponse | None,
    status_code=status.HTTP_200_OK,
    description="Get activist's session, if he's in one of them",
)
@inject
def getInSession(
        id: UUID,
        user: AuthUser = Depends(AuthRequireRoles(AuthRole.Activist)),
):
    pass


@router.put(
    "/{id}/join/{sessionId}",
    response_model=ActivistSessionResponse,
    status_code=status.HTTP_200_OK,
    description="Join a session. Available to activist itself only",
)
@inject
def joinSession(
        id: UUID,
        sessionId: UUID,
        user: AuthUser = Depends(AuthRequireRoles(AuthRole.Activist)),
):
    pass
