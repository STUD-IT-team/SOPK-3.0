from dependency_injector.wiring import Provide, inject
from injection import Container
from aiogram import Dispatcher

from handlers.echo import EchoRouter

@inject
def setupHandlers(dp: Dispatcher = Provide[Container.mainDispatcher]):
    dp.include_router(EchoRouter)