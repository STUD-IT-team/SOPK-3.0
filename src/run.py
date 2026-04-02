from fastapi import FastAPI

from injection import Container
from api import mount_routers


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(title="My App")
    app.container = container

    container.wire(
        modules=[__name__,],
        packages=["api"]
    )

    mount_routers(app)


    return app

app = create_app()