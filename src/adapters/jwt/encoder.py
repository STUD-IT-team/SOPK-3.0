import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID

from services.auth import AuthCredentialsEncoder, DecodeSecurityError, EncodeError

__all__ = ["JwtAuthCredentialsEncoder"]

class JwtAuthCredentialsEncoder(AuthCredentialsEncoder):
    def __init__(self, secret: str, algorithm: str = "HS256", expires_minutes: int = 60):
        self.secret = secret
        self.algorithm = algorithm
        self.expires_minutes = expires_minutes

    def Encode(self, user_id: UUID) -> str:
        try:
            payload = {
                "sub": str(user_id),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expires_minutes),
                "iat": datetime.now(timezone.utc),
            }

            token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
            return token

        except Exception as e:
            raise EncodeError(str(e))

    def Decode(self, credentials: str) -> UUID:
        try:
            payload = jwt.decode(credentials, self.secret, algorithms=[self.algorithm])

            user_id = payload.get("sub")
            if user_id is None:
                raise DecodeSecurityError("Missing subject")

            return UUID(user_id)

        except jwt.ExpiredSignatureError:
            raise DecodeSecurityError("Token expired")

        except jwt.InvalidTokenError as e:
            raise DecodeSecurityError(str(e))