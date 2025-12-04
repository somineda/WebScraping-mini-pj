from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.diary import router as diary_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(diary_router)