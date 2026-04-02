from fastapi import FastAPI

from .auth import AuthRouter

def mount_routers(app: FastAPI) -> None:
    app.include_router(AuthRouter)
