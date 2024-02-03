import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

import config
import handlers
from middlewares.middlewares import DbSessionMiddleware
from redis.asyncio import Redis

load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Получение экземпляра логгера
redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=RedisStorage(redis))
    dp.include_router(handlers.router)
    engine = create_async_engine(
        'postgresql+asyncpg://postgres:Fallout@localhost/postgres', echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=sessionmaker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=sessionmaker,
                           allowed_updates=dp.resolve_used_update_types())
    logger.info('Bot started')  # Переместите этот вызов внутрь main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
