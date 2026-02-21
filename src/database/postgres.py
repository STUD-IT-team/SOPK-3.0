from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text
import asyncio

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
        url = f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
        self._engine = create_async_engine(url, echo=config.echo)
        if not asyncio.get_event_loop().is_running():
            asyncio.run(self._ping())
        else:
            asyncio.create_task(self._ping())
        self._session = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession
        )
    
    def get_session(self) -> AsyncSession:
        return self._session()
    
    async def _ping(self):
        async with self._engine.connect() as conn:
            await conn.execute(text("SELECT 1"))