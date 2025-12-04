from fastapi import HTTPException, status

from app.models import Diary, User
from app.repositories.diary import DiaryRepository
from app.schemas import DiaryCreate, DiaryUpdate


class DiaryService:
    @staticmethod #같은 날짜에 이미 일기가 있는지 확인
    async def create(user: User, data: DiaryCreate) -> Diary:
        existing = await DiaryRepository.get_by_user_and_date(user, data.date)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 같은 날짜에 일기가 존재합니다",
            )

        return await DiaryRepository.create(
            user=user,
            title=data.title,
            content=data.content,
            date=data.date,
        )

    @staticmethod
    async def get_list(user: User) -> list[Diary]:
        return await DiaryRepository.get_by_user(user)

    @staticmethod
    async def get_detail(user: User, diary_id: int) -> Diary:
        diary = await DiaryRepository.get_by_id(diary_id)

        if not diary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="일기를 찾을 수 없습니다",
            )

        #작성자 본인확인
        if diary.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="권한이 없습니다",
            )

        return diary

    @staticmethod
    async def update(user: User, diary_id: int, data: DiaryUpdate) -> Diary:
        diary = await DiaryRepository.get_by_id(diary_id)

        if not diary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="일기를 찾을 수 없습니다!",
            )

        #작성자 본인 확인
        if diary.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="일기 작성 권한이 없습니다!",
            )

        return await DiaryRepository.update(
            diary,
            title=data.title,
            content=data.content,
            date=data.date,
        )

    @staticmethod
    async def delete(user: User, diary_id: int) -> None:
        diary = await DiaryRepository.get_by_id(diary_id)

        if not diary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="일기를 찾을 수가 없습니다.",
            )

        #작성자 본인 확인
        if diary.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="일기 삭제 권한이 없습니다!y",
            )

        await DiaryRepository.delete(diary)