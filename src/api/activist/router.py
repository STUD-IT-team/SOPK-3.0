from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from dependency_injector.wiring import inject, Provide
from injection import Container
from api.activist.dto import ActivistResponse, AllActivistResponse, UpdateActivistDataDto, ActivistSessionResponse, \
    UpdateActivistTimeslotDto
from api import AuthRequireRoles, OrganizerOrActivistItself, AuthRequireRolesOrUserItself
from services.auth import AuthRole
from services.activist import ActivistService, UpdateDataDto as ServiceUpdateDataDto, TimeslotNotFoundError, \
    TimeslotAlreadyFullError, SessionNotFoundError, SessionAlreadyFinishedError, AlreadyJoinedSessionError

router = APIRouter(prefix="/activist", tags=["Activist"])


@router.get(
    "/",
    response_model=AllActivistResponse,
    status_code=status.HTTP_200_OK,
    description="Get all activists",
    dependencies=[Depends(AuthRequireRoles(AuthRole.Organizer))]
)
@inject
async def getAll(service: ActivistService = Depends(Provide[Container.activistService])):
    activists = await service.getAll()
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
        service: ActivistService = Depends(Provide[Container.activistService]),
):
    activist = await service.getById(id)
    return activist
        

@router.put(
    "/{id}/data",
    dependencies=[Depends(AuthRequireRolesOrUserItself(owner_role=AuthRole.Activist))],
    status_code=status.HTTP_200_OK,
    response_model=ActivistResponse,
    description="Update an activist information (form). Available to activist itself only",
)
@inject
async def updateData(
        id: UUID, 
        data: UpdateActivistDataDto,
        service: ActivistService = Depends(Provide[Container.activistService]),
):
    serviceDto = ServiceUpdateDataDto(**data.model_dump())
    return await service.updateData(id, serviceDto)


@router.put(
    "/{id}/timeslot",
    dependencies=[Depends(OrganizerOrActivistItself)],
    status_code=status.HTTP_200_OK,
    response_model=ActivistResponse,
    description="Update (or firstly set) activist's timeslot. Available to activist itself or organizer",
)
@inject
async def updateTimeslot(
        id: UUID,
        data: UpdateActivistTimeslotDto,
        service: ActivistService = Depends(Provide[Container.activistService]),
):
    try:
        activist = await service.updateTimeslot(id, data.TimeslotID)
    except TimeslotNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeslot not found"
        )
    except TimeslotAlreadyFullError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Timeslot is already full"
        )
        
    return activist


@router.delete(
    "/{id}",
    dependencies=[Depends(AuthRequireRoles(AuthRole.Admin))],
    status_code=status.HTTP_200_OK,
    description="Delete an activist. Available to admin only",
)
@inject
async def delete(id: UUID, service: ActivistService = Depends(Provide[Container.activistService])):
    await service.delete(id)


@router.get(
    "/{id}/session",
    dependencies=[Depends(AuthRequireRolesOrUserItself(owner_role=AuthRole.Activist))],
    response_model=ActivistSessionResponse | None,
    status_code=status.HTTP_200_OK,
    description="Get activist's session, if he's in one of them",
)
@inject
async def getInSession(
        id: UUID,
        service: ActivistService = Depends(Provide[Container.activistService]),
):
    return await service.getInSession(id)


@router.put(
    "/{id}/join/{sessionId}",
    dependencies=[Depends(AuthRequireRolesOrUserItself(owner_role=AuthRole.Activist))],
    response_model=ActivistSessionResponse,
    status_code=status.HTTP_200_OK,
    description="Join a session. Available to activist itself only",
)
@inject
async def joinSession(
        id: UUID,
        sessionId: UUID,
        service: ActivistService = Depends(Provide[Container.activistService])
):
    try:
        session = await service.joinSession(id, sessionId)
    except SessionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    except SessionAlreadyFinishedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session is already finished"
        )
    except AlreadyJoinedSessionError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already in a session"
        )
        
    return session
