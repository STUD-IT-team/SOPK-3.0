from typing import Type, Dict, Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from database import PostgresDatabase
from models import UnitOfWork, Repository

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db: PostgresDatabase, repo_map: Dict[Type, Type]):
        self._db = db
        self._repo_map = repo_map

        self.session: AsyncSession | None = None
        self._repos: Dict[Type, Any] = {}

    async def __aenter__(self) -> UnitOfWork:
        self._ctx = self._db.get_session()
        self.session = await self._ctx.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self.rollback()
        else:
            await self.commit()

        await self._ctx.__aexit__(exc_type, exc, tb)

    async def commit(self):
        await self.session.flush()
        await self.session.commit()


    async def rollback(self):
        await self.session.rollback()

    def _get_repo(self, repo_type: Type[Repository]) -> Repository:
        if self.session is None:
            raise RuntimeError("UnitOfWork not entered")

        if repo_type not in self._repos:
            repo_class = self._repo_map[repo_type]
            self._repos[repo_type] = repo_class(self.session)

        return cast(Repository, self._repos[repo_type])

    def get(self, t: Type[Repository]) -> Repository:
        return self._get_repo(t)