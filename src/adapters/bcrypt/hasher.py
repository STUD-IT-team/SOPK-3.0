import bcrypt

from services.auth import PasswordHasher

__all__ = ["BcryptPasswordHasher"]

class BcryptPasswordHasher(PasswordHasher):
    def HashPassword(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")

    def HashAndCompare(self, password: str, hashed: str) -> bool:
        password_bytes = password.encode("utf-8")
        hashed_bytes = hashed.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hashed_bytes)