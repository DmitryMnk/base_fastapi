from logging import DEBUG, ERROR, INFO, WARNING
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class LoggingSettings(BaseSettings):
    """Класс настроек логирования.

    Этот класс используется для хранения и управления настройками логирования
    приложения. Он наследуется от `BaseSettings`, что позволяет загружать
    настройки из переменных окружения.

    Атрибуты:
        LOGGER_NAME (str): Имя логгера. По умолчанию "appLogger".
        LEVEL (str): Уровень логирования. По умолчанию "DEBUG".
            Доступные уровни: "DEBUG", "INFO", "WARNING", "ERROR".
        INTERVAL (int): Интервал ротации логов в днях. По умолчанию 1.
        BACKUP_COUNT (int): Количество резервных копий логов. По умолчанию 30.
        ENCODING (str): Кодировка файлов логов. По умолчанию "utf-8".
        DISABLE_STREAM (bool): Указывает, следует ли отключить вывод логов в поток.
            По умолчанию False.

    Методы:
        log_path (str): Возвращает путь к директории для хранения логов.
            Директория создается, если она не существует.
        log_level (int): Возвращает уровень логирования в виде целого
            числа, соответствующего заданному уровню.
    """

    model_config = SettingsConfigDict(extra="ignore", env_prefix="LOGGING_")
    LOGGER_NAME: str = "appLogger"
    LEVEL: str = "DEBUG"
    INTERVAL: int = 1
    BACKUP_COUNT: int = 30
    ENCODING: str = "utf-8"
    DISABLE_STREAM: bool = False

    @property
    def log_path(self) -> str:
        """Возвращает путь к директории для хранения логов.

        Директория создается, если она не существует.

        :return: Путь к директории для логов.
        """
        log_dir: Path = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        return str(log_dir)

    @property
    def log_level(self) -> int:
        """Возвращает уровень логирования в виде целого числа.
        Если заданный уровень не поддерживается, возвращает уровень DEBUG.

        :return: Уровень логирования.
        """
        levels = {
            "DEBUG": DEBUG,
            "INFO": INFO,
            "WARNING": WARNING,
            "ERROR": ERROR,
        }
        level = levels.get(self.LEVEL)
        if not level:
            return DEBUG
        return level


class PostgresSettings(BaseSettings):
    """Класс настроек PostgreSQL.

    Этот класс используется для хранения и управления настройками
    подключения к базе данных PostgreSQL. Он наследуется от
    `BaseSettings`, что позволяет загружать  настройки из переменных
    окружения.
    """

    model_config = SettingsConfigDict(extra="ignore", env_prefix="POSTGRES_")
    USER: str = "user"
    PASSWORD: str = "password"
    HOST: str = "db"
    PORT: int = 5432
    NAME: str = "defaultdb"
    DRIVER: str = "postgresql+asyncpg"
    AUTOFLUSH: bool = False
    AUTOCOMMIT: bool = False
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    POOL_PRE_PING: bool = True
    ECHO: bool = False
    EXPIRE_ON_COMMIT: bool = False

    def get_connection_url(self) -> URL:
        """Возвращает URL соединения к PostgreSQL.

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
        """Возвращает строку соединения к PostgreSQL.

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
    """Класс настроек приложения."""

    model_config = SettingsConfigDict(extra="ignore", env_prefix="APP_")
    POSTGRES: PostgresSettings = PostgresSettings()
    LOGGING: LoggingSettings = LoggingSettings()
    API_PREFIX: str = "/api/service"
    DEBUG: bool = True


settings = AppSettings()
