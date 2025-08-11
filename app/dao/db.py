from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.dao.database import Base


async def create_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS tronlogs;"))
