from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text
import asyncio

from contextlib import asynccontextmanager

class PostgresConfig:
    def __init__(self, host, port, user, password, database, echo = False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.echo = echo

class PostgresDatabase:
    def __init__(self, config):
        self._config = config
        self._engine = None
        self._sessionmaker = None

    def _init_engine(self):
        if self._engine is None:
            url = (
                f"postgresql+asyncpg://"
                f"{self._config.user}:{self._config.password}"
                f"@{self._config.host}:{self._config.port}"
                f"/{self._config.database}"
            )
            self._engine = create_async_engine(
                url,
                echo=self._config.echo,
            )
            self._sessionmaker = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        self._init_engine()
        async with self._sessionmaker() as session:
            yield session

    async def ping(self):
        self._init_engine()
        async with self._engine.connect() as conn:
            await conn.execute(text("SELECT 1"))