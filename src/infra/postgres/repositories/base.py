
from database.postgres import PostgresDatabase


class BaseRepository:
    def __init__(self, db: PostgresDatabase):
        self._db = db