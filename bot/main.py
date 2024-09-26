import asyncio
from time import sleep
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database.engine_db import init_db
from handlers import  photo
from aiogram.client.session.aiohttp import AiohttpSession


from config import settings

dp = Dispatcher(storage=MemoryStorage())

async def main() -> None:
    await init_db()
    sleep(3)
    session = AiohttpSession()
    bot = Bot(settings.telegram.token, session=session)
    dp.include_routers(
        photo.router,
    )
    await dp.start_polling(bot)
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())