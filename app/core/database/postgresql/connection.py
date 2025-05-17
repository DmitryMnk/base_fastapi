from typing import Any, AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ...config import settings


class PSQLConnectionManager:
    """Класс менеджер соединений с PostgreSQL.

    Этот класс управляет созданием и использованием асинхронных сессий
    для работы с базой данных PostgreSQL.
    Он использует SQLAlchemy для управления соединениями и сессиями.
    """

    def __init__(self, url: URL):
        self.url = url
        self.engine = create_async_engine(url=self.url)
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        """
        Возвращает объект async_sessionmaker.
        :return: Объект, используемый для создания асинхронных сессий.
        """
        session: async_sessionmaker[AsyncSession] = self.session_maker
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Генератор асинхронной сессии.

        Этот метод создает асинхронную сессию, управляет ее жизненным циклом
        и обеспечивает автоматическую фиксацию или откат транзакции в случае ошибки.

        :yields: AsyncSession - Асинхронная сессия для работы с базой данных.
        :rises: Exception - Если происходит ошибка во время работы с сессией,
                транзакция будет откатана.
        :return:
        """
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


psql_connection_manager = PSQLConnectionManager(settings.POSTGRES.get_connection_url())
