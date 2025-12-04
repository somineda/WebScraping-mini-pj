from datetime import datetime

from app.models import TokenBlacklist


class TokenRepository:
    @staticmethod
    async def add_to_blacklist(token: str, expires_at: datetime) -> TokenBlacklist:
        return await TokenBlacklist.create(token=token, expires_at=expires_at)

    @staticmethod
    async def is_blacklisted(token: str) -> bool:
        exists = await TokenBlacklist.filter(token=token).exists()
        return exists