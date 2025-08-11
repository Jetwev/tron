from typing import Sequence

from loguru import logger
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.tron.models import TronLog


class TronLogDAO(BaseDAO):
    model = TronLog

    @classmethod
    async def add(cls, session: AsyncSession, data: BaseModel) -> TronLog:
        data_dict = data.model_dump()
        logger.info(f"Add a new record {cls.model.__name__} with: {data_dict}")
        try:
            new_instance = cls.model(**data_dict)
            session.add(new_instance)
            logger.info(f"Record {cls.model.__name__} was added")
            await session.flush()
            return new_instance
        except SQLAlchemyError as e:
            logger.error(f"Error while adding a new record: {e}")
            raise

    @classmethod
    async def extract(cls, session: AsyncSession, page: int, per_page: int) -> Sequence:
        offset = (page - 1) * per_page
        logger.info(f"Return last records {cls.model.__name__} with {offset=}")
        try:
            query = select(cls.model).order_by(cls.model.created_at.desc()).offset(offset).limit(per_page)
            print(query)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Records were found: {len(records)}")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Error while extracting data: {e}")
            raise
