from dependency_injector.wiring import Provide, inject
from injection import Container

from middlewares.log import LogMiddleware
from aiogram import Dispatcher


@inject
async def setupMiddlewares(dp: Dispatcher = Provide[Container.mainDispatcher]):
    dp.update.outer_middleware(LogMiddleware())
