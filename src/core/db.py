from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)


class Base(DeclarativeBase):
    pass


class Database:

    def __init__(self) -> None:
        self.engine = create_async_engine(
            url="sqlite+aiosqlite:///database.db"
        )
        self._session_maker = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    async def create_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def create_async_session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession
        try:
            async with self._session_maker() as session:
                yield session
        except Exception as e:
            await session.rollback()


database = Database()
