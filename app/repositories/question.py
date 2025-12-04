import random

from app.models import DailyQuestion


class QuestionRepository:
    @staticmethod
    async def get_random() -> DailyQuestion | None:
        questions = await DailyQuestion.all()
        if not questions:
            return None
        return random.choice(questions)

    @staticmethod
    async def get_random_by_category(category: str) -> DailyQuestion | None:
        questions = await DailyQuestion.filter(category=category)
        if not questions:
            return None
        return random.choice(questions)

    @staticmethod
    async def get_all() -> list[DailyQuestion]:
        return await DailyQuestion.all()

    @staticmethod
    async def get_categories() -> list[str]:
        questions = await DailyQuestion.all().distinct().values_list("category", flat=True)
        return [q for q in questions if q]