import asyncio
import logging

from aiogram import Dispatcher

from common import bot
from db.base import create_session
from middlewares import DbSessionMiddleware
from routers.commands import client_commands
from routers.menu import client_menu_callbacks, client_ai_menu

# Логирование
logging.basicConfig(level=logging.INFO)

async def main():
    sessionmaker = await create_session()

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_router(client_commands.router)
    dp.include_router(client_menu_callbacks.router)
    dp.include_router(client_ai_menu.router)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())