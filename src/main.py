import asyncio
import logging

import sys
from pathlib import Path

from aiogram import Bot, Dispatcher

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from src.core import database as db
from src.routers import main_router
from src.config import Settings


def init_logging(settings: Settings) -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


async def create_db() -> None:
    await db.create_db()


async def start_bot(settings: Settings) -> None:
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)
    await dp.start_polling(bot)


async def main() -> None:
    settings = Settings()
    init_logging(settings)
    await create_db()
    await start_bot(settings)


if __name__ == "__main__":
    asyncio.run(main())
