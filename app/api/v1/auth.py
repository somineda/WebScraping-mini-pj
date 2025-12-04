from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.deps import get_current_user
from app.models import User
from app.repositories.token import TokenRepository
from app.schemas import Token, UserCreate, UserResponse
from app.schemas.user import UserLogin
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()

#회원가입
@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate):
    user = await AuthService.register(data)
    return user

#로그인
@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    access_token = await AuthService.login(data)
    return Token(access_token=access_token)

#로그아웃
@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user),
):
    token = credentials.credentials
    expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    await TokenRepository.add_to_blacklist(token, expires_at)
    return {"message": "Successfully logged out"}

#현재 로그인된 사용자 정보 확인
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user