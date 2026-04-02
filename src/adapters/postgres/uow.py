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
        self._ctx = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self._ctx = self._db.get_session()
        self.session = await self._ctx.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            if exc:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self._ctx.__aexit__(exc_type, exc, tb)
            await  self.session.close()
            self.session = None
            self._repos.clear()

    async def commit(self):
        if self.session is None:
            raise RuntimeError("UoW not entered")
        await self.session.flush()
        await self.session.commit()

    async def rollback(self):
        if self.session is None:
            raise RuntimeError("UoW not entered")
        await self.session.rollback()

    def get(self, repo_type: Type[Repository]) -> Repository:
        if self.session is None:
            raise RuntimeError("UoW not entered")

        if repo_type not in self._repos:
            if repo_type not in self._repo_map:
                raise KeyError(f"Repository {repo_type} not registered")

            repo_class = self._repo_map[repo_type]
            self._repos[repo_type] = repo_class(self.session)

        return cast(Repository, self._repos[repo_type])