from functools import wraps
from typing import Any, Callable

from app.dao.database import async_session_maker


def connection(commit: bool = True) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async with async_session_maker() as session:
                try:
                    result = await method(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()
        return wrapper
    return decorator
