from datetime import date as date_type

from app.models import Diary, User


class DiaryRepository:
    @staticmethod
    async def create(user: User, title: str, content: str, date: date_type) -> Diary:
        return await Diary.create(
            user=user,
            title=title,
            content=content,
            date=date,
        )

    @staticmethod
    async def get_by_id(diary_id: int) -> Diary | None:
        return await Diary.filter(id=diary_id).first()

    @staticmethod
    async def get_by_user(user: User) -> list[Diary]:
        return await Diary.filter(user=user).order_by("-date")

    @staticmethod
    async def get_by_user_and_date(user: User, date: date_type) -> Diary | None:
        return await Diary.filter(user=user, date=date).first()

    @staticmethod
    async def update(diary: Diary, **kwargs) -> Diary:
        for key, value in kwargs.items():
            if value is not None:
                setattr(diary, key, value)
        await diary.save()
        return diary

    @staticmethod
    async def delete(diary: Diary) -> None:
        await diary.delete()