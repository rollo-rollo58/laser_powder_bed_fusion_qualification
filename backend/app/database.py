"""SQLAlchemy async session factory for optional PostgreSQL persistence."""
from __future__ import annotations

from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from .config import load_settings


_ENGINE = None
_SESSION = None


def session_factory() -> async_sessionmaker[AsyncSession]:
    global _ENGINE, _SESSION
    if _SESSION is None:
        _ENGINE = create_async_engine(
            load_settings().database_url,
            pool_pre_ping=True,
            echo=False,
        )
        _SESSION = async_sessionmaker(_ENGINE, expire_on_commit=False)
    return _SESSION


async def get_session() -> AsyncIterator[AsyncSession]:
    factory = session_factory()
    async with factory() as session:
        yield session


async def close_engine() -> None:
    global _ENGINE, _SESSION
    if _ENGINE is not None:
        await _ENGINE.dispose()
    _ENGINE = None
    _SESSION = None
