from abc import ABC

__all__ = ["PasswordHasher"]

class PasswordHasher(ABC):
    def HashPassword(self, password: str) -> str:
        raise NotImplementedError

    def HashAndCompare(self, password: str, hashed: str) -> bool:
        raise NotImplementedError
