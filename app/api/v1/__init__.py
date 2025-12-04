from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.diary import router as diary_router
from app.api.v1.quotes import router as quote_router
from app.api.v1.question import router as question_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(diary_router)
router.include_router(quote_router)
router.include_router(question_router)