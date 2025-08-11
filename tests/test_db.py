import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from app.dao.db import create_db, drop_db
from app.tron.dao import TronLogDAO
from app.tron.schemas import TronLogPydantic


@pytest.fixture(scope="session")
def postgres_container():
    container = PostgresContainer("postgres:15")
    container.start()
    url = container.get_connection_url()
    async_url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    yield async_url
    container.stop()


@pytest.fixture(scope="session")
def engine(postgres_container):
    return create_async_engine(postgres_container)


@pytest_asyncio.fixture(autouse=True)
async def setup_db(engine):
    await create_db(engine)
    yield
    await drop_db(engine)


@pytest.mark.asyncio
async def test_tronlog_add_extract(engine):
    test_data = TronLogPydantic(
        address="TQ6WzMFdAZFLxnC2yJ9J4FRgj6uR8v1v7M",
        balance=1000,
        bandwidth=5000,
        energy=10000,
    )
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        result = await TronLogDAO.add(session=session, data=test_data)
        await session.commit()

        assert result.address == test_data.address

    async with async_session() as session:
        records = await TronLogDAO.extract(session, page=1, per_page=10)

        assert len(records) == 1
