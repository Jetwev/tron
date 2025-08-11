from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.database import Base


T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T] | None = None

    def __init__(self, session: AsyncSession):
        if self.model is None:
            raise ValueError("Model should be defined...")
