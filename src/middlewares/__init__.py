from dependency_injector.wiring import Provide, inject
from injection import Container

from .log import LogMiddleware
from .role import RoleMiddleware
from aiogram import Dispatcher


@inject
async def setupMiddlewares(dp: Dispatcher = Provide[Container.mainDispatcher]):
    dp.update.outer_middleware(LogMiddleware())
    dp.update.outer_middleware(RoleMiddleware())
