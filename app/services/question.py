from fastapi import HTTPException, status

from app.models import DailyQuestion
from app.repositories.question import QuestionRepository


class QuestionService:
    @staticmethod
    async def get_random(category: str | None = None) -> DailyQuestion:
        if category:
            question = await QuestionRepository.get_random_by_category(category)
        else:
            question = await QuestionRepository.get_random()

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions available. Please seed questions first.",
            )
        return question

    @staticmethod
    async def get_all() -> list[DailyQuestion]:
        return await QuestionRepository.get_all()

    @staticmethod
    async def get_categories() -> list[str]:
        return await QuestionRepository.get_categories()