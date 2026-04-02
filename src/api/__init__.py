from fastapi import FastAPI

from .auth import AuthRouter, AuthCurrentUser, AuthRequireRole
from .session import SessionRouter
from .activist import  ActivistRouter
from .organizer import OrganizerRouter
from .timeslot import TimeslotRouter

def mount_routers(app: FastAPI) -> None:
    app.include_router(AuthRouter)
    app.include_router(SessionRouter)
    app.include_router(ActivistRouter)
    app.include_router(OrganizerRouter)
    app.include_router(TimeslotRouter)
