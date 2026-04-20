from fastapi import APIRouter, Depends, HTTPException, status

from dependency_injector.wiring import inject, Provide
from injection import Container

from uuid import UUID

from api import AuthCurrentUser, AuthRequireRoles

from .dto import (
    SessionResponse,
    AllSessionResponse,
    AssessmentResponse,
    UpdateAssessmentDto, CanEndResponse, AllAssessmentResponse,
)

from api import AuthCurrentUser, AuthRequireRoles
from services.auth import AuthUser, AuthRole

router = APIRouter(prefix="/session", tags=["Session"])


@router.get(
    "/",
    description="Get all sessions. Available for Admin only.",
    status_code=status.HTTP_200_OK,
    response_model=AllSessionResponse,
)
@inject
def getAll(
        user: AuthUser = Depends(AuthRequireRoles(AuthRole.Admin)),
):
    pass


@router.get(
    "/:id",
    description="Get session by ID. Available for Admin only.",
    status_code=status.HTTP_200_OK,
    response_model=SessionResponse,
)
@inject
def getById(
    id: UUID,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Admin)),
):
    pass


@router.delete(
    "/:id", description="Delete session by ID. Available for Admin Only", status_code=status.HTTP_200_OK
)
@inject
def delete(
    id: UUID,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Admin)),
):
    pass


@router.post(
    "/start",
    description="Start a new session. Available for Organizers",
    status_code=status.HTTP_201_CREATED,
    response_model=SessionResponse,
)
@inject
def startSession(
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Organizer)),
):
    pass


@router.get(
    "/end",
    description="Check if session can be ended. Available to organizer, who created session",
    status_code=status.HTTP_200_OK,
    response_model=CanEndResponse,
)
@inject
def canEnd(
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Organizer)),
):
    pass


@router.post(
    "/end",
    description="End the current session. Available to organizer, who created session",
    status_code=status.HTTP_200_OK,
    response_model=SessionResponse,
)
@inject
def endSession(
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Organizer)),
):
    pass


@router.get(
    "/:id/assessment/:activistId",
    description="Get assessment for activist in session, created by current organizer",
    status_code=status.HTTP_200_OK,
    response_model=AssessmentResponse,
)
@inject
def getAssessment(
    id: UUID,
    activistId: UUID,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Organizer)),
):
    pass

@router.get(
    "/:id/assessment",
    description="Get all assessments in session. Available for Organizer, who create session.",
    status_code=status.HTTP_200_OK,
    response_model=AllAssessmentResponse,
)
@inject
def getAllAssessments(
    id: UUID,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Organizer)),
):
    pass


@router.put(
    "/:id/assessment/:activistId",
    description="Update assessment for activist in session. Available to organizer in session",
    status_code=status.HTTP_200_OK,
    response_model=AssessmentResponse,
)
@inject
def updateAssessment(
    id: UUID,
    activistId: UUID,
    data: UpdateAssessmentDto,
    user: AuthUser = Depends(AuthRequireRoles(AuthRole.Organizer)),
):
    pass
