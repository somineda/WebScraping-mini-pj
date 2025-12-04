from fastapi import APIRouter, Query

from app.schemas import QuestionResponse
from app.scraping.questions import seed_questions
from app.services.question import QuestionService

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post(
    "/seed",
    summary="질문 데이터 추가",
    description="자기성찰 질문 80개를 DB에 추가",
)
async def seed_question_data():
    result = await seed_questions()
    return result


@router.get(
    "/random",
    response_model=QuestionResponse,
    summary="랜덤 질문 조회",
    description="랜덤으로 자기성찰 질문 1개 조회 카테고리 필터 가능",
)
async def get_random_question(
    category: str | None = Query(default=None, description="질문 카테고리 필터"),
):
    question = await QuestionService.get_random(category)
    return question


@router.get(
    "",
    response_model=list[QuestionResponse],
    summary="전체 질문 조회",
    description="DB에 저장된 모든 질문 조회",
)
async def get_all_questions():
    questions = await QuestionService.get_all()
    return questions


@router.get(
    "/categories",
    response_model=list[str],
    summary="질문 카테고리 목록 조회",
    description="사용 가능한 질문 카테고리 목록",
)
async def get_categories():
    categories = await QuestionService.get_categories()
    return categories