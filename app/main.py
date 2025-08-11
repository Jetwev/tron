from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI, Request, Response
from loguru import logger

from app.api.router import api_router
from app.dao.database import engine
from app.dao.db import create_db, drop_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    try:
        logger.info("Initialization...")
        await drop_db(engine)
        await create_db(engine)
        yield
    except Exception as e:
        logger.error(f"Some error with initialization: {e}")
    finally:
        logger.info("Shutting down...")


def register_routers(app: FastAPI) -> None:
    root_router = APIRouter()

    @root_router.get("/")
    async def healthcheck(request: Request, response: Response) -> dict:
        return {
            "status": "ok"
        }

    app.include_router(root_router)
    app.include_router(api_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Application",
        version="1.0.0",
        lifespan=lifespan,
    )

    register_routers(app)
    return app


app = create_app()
