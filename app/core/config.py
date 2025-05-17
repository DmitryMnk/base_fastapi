from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class PostgresSettings(BaseSettings):
    """Класс настроек PostgreSQL"""

    model_config = SettingsConfigDict(extra="ignore", env_prefix="POSTGRES_")
    USER: str = "user"
    PASSWORD: str = "password"
    HOST: str = "db"
    PORT: int = 5432
    NAME: str = "defaultdb"
    DRIVER: str = "postgresql+asyncpg"

    def get_connection_url(self) -> URL:
        """
        Возвращает URL соединения к PostgreSQL.

        Этот метод создает и возвращает объект URL, который содержит
        информацию о соединении с базой данных PostgreSQL, включая
        драйвер, имя пользователя, пароль, хост, порт и имя базы данных.
        :return: Объект URL, представляющий строку соединения к PostgreSQL.
        """

        return URL.create(
            drivername=self.DRIVER,
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            database=self.NAME,
        )

    def get_connection_string(self) -> str:
        """
        Возвращает строку соединения к PostgreSQL.

        Этот метод формирует и возвращает строку соединения, которая
        может быть использована для подключения к базе данных PostgreSQL.
        Строка включает в себя драйвер, имя пользователя, пароль, хост,
        порт и имя базы данных.
        :return: Строка соединения к PostgreSQL.
        """
        return (
            f"{self.DRIVER}://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class AppSettings(BaseSettings):
    """Класс настроек приложения"""

    model_config = SettingsConfigDict(extra="ignore", env_prefix="APP_")
    POSTGRES: PostgresSettings = PostgresSettings()
    API_PREFIX: str = "/api/service"
    DEBUG: bool = True


settings = AppSettings()
