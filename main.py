import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from sqlalchemy.engine import URL

import config
from handlers import router
from middlewares.middlewares import DbSessionMiddleware


load_dotenv()


async def main(logger):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    postgres_url = URL.create(
        'postgresql+asyncpg',
        username=os.getenv("POSTGRES_USER"),
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv("POSTGRES_DB"),
        port=int(os.getenv("POSTGRES_PORT")),
        password=os.getenv('POSTGRES_PASSWORD')
    )

    engine = create_async_engine('postgresql+asyncpg://postgres:Fallout@localhost/postgres', echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=sessionmaker, logger=logger,
                           allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logger = logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main(logger))
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
