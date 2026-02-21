from dataclasses import dataclass
from abc import ABC

__all__ = ["MainOrganizer", "MainOrganizerRepository"]

@dataclass
class MainOrganizer:
    TgID: int
    TgNick: str
    FullName: str


class MainOrganizerRepository(ABC):
    def get(self, id: int) -> MainOrganizer:
        raise NotImplementedError

    def save(self, model: MainOrganizer) -> MainOrganizer:
        raise NotImplementedError
