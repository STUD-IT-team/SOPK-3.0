from fastapi import FastAPI

from injection import Container
from api import mount_routers

import uvicorn


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

uvicorn.run(app, host="0.0.0.0", port=8000)