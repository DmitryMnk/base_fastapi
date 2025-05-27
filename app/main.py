from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from core import settings
from services import startup_app
from services.middlewares import setup_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Управляет жизненным циклом приложения FastAPI.

    Эта асинхронная контекстная функция используется для выполнения
    операций при запуске и завершении работы приложения.

    :param app: Экземпляр приложения FastAPI, для которого
        управляется жизненный цикл.
    """
    startup_app()
    yield


app = FastAPI(
    docs_url=settings.API_PREFIX + "/docs",
    redoc_url=settings.API_PREFIX + "/redoc",
    openapi_url=settings.API_PREFIX + "/openapi.json",
    lifespan=lifespan,
)

setup_middlewares(app)
