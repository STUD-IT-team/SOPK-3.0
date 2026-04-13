from fastapi import APIRouter, Depends, HTTPException, status

from dependency_injector.wiring import inject, Provide
from injection import Container

from uuid import UUID

from api import AuthCurrentUser, AuthRequireRoles

from .dto import TimeslotResponse, AllTimeslotResponse, CreateTimeslotDto

from api import AuthCurrentUser, AuthRequireRoles
from services.auth import AuthUser, AuthRole

router = APIRouter(prefix="/timeslot", tags=["Timeslot"])


@router.get(
    "/",
    description="Get all timeslots. Available to everyone.",
    status_code=status.HTTP_200_OK,
    response_model=AllTimeslotResponse,
)
@inject
async def getAll(
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Activist)),
):
    pass


@router.get(
    "/:id",
    description="Get timeslot by ID. Available to everyone.",
    status_code=status.HTTP_200_OK,
    response_model=TimeslotResponse,
)
@inject
async def get(
    id: UUID,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Activist)),
):
    pass


@router.post(
    "/",
    description="Create a new timeslot. Available to Admin.",
    status_code=status.HTTP_201_CREATED,
    response_model=TimeslotResponse,
)
@inject
async def post(
    data: CreateTimeslotDto,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Activist)),
):
    pass


@router.delete(
    "/:id",
    description="Delete timeslot by ID. Available to Admin.",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete(
    id: UUID,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Admin)),
):
    pass


# Think about it later. Probably formdata or smth.
@router.post(
    "/excel", description="Import timeslots from Excel. Available to Admin.",
    status_code=status.HTTP_200_OK,

)
@inject
async def excel(
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Admin)),
):
    pass
