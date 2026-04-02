from abc import ABC
from uuid import UUID

__all__ = ["AuthCredentialsEncoder", "DecodeSecurityError", "EncodeError"]

class AuthCredentialsEncoder(ABC):
    def Encode(self, user_id: UUID) -> str:
        pass

    def Decode(self, credentials: str) -> UUID:
        pass


class DecodeSecurityError(Exception):
    pass

class EncodeError(Exception):
    pass
