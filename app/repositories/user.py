from app.models import User


class UserRepository:
    @staticmethod
    async def get_by_email(email: str) -> User | None:
        return await User.filter(email=email).first()

    @staticmethod
    async def get_by_id(user_id: int) -> User | None:
        return await User.filter(id=user_id).first()

    @staticmethod
    async def create(email: str, username: str, hashed_password: str) -> User:
        return await User.create(
            email=email,
            username=username,
            password=hashed_password,
        )