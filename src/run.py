from dependency_injector.wiring import inject, Provide
from aiogram import Bot, Dispatcher
from injection import Container

import asyncio

@inject
async def main(
    bot: Bot = Provide[Container.bot],
    dp: Dispatcher = Provide[Container.mainDispatcher]
) -> None:
    import handlers
    handlers.setupHandlers()

    import middlewares
    await middlewares.setupMiddlewares()

    try:    
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    container = Container()
    container.wire(
        modules=[__name__],
        packages=["handlers", "middlewares", "handlers.utils"],
    )
    
    asyncio.run(main())