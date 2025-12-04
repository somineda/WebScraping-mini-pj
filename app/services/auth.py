from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.user import UserRepository
from app.schemas import UserCreate, UserLogin


class AuthService:
    @staticmethod
    async def register(data: UserCreate) -> User: #이메일 중복 확인
        existing_user = await UserRepository.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        #비번 해시화 해서 저장
        hashed_password = hash_password(data.password)
        user = await UserRepository.create(
            email=data.email,
            username=data.username,
            hashed_password=hashed_password,
        )
        return user

    @staticmethod
    async def login(data: UserLogin) -> str: #사용자 조회
        user = await UserRepository.get_by_email(data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

#비밀번호 확인
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(user.id)
        return access_token