from fastapi import HTTPException, status

from app.models import Quote, QuoteBookmark, User
from app.repositories.quotes import QuoteBookmarkRepository, QuoteRepository


class QuoteService:
    @staticmethod
    async def get_random() -> Quote:
        quote = await QuoteRepository.get_random()
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="명언이 존재하지 않습니다",
            )
        return quote

    @staticmethod
    async def get_all() -> list[Quote]:
        return await QuoteRepository.get_all()


class QuoteBookmarkService:
    @staticmethod
    async def add_bookmark(user: User, quote_id: int) -> QuoteBookmark:
        quote = await QuoteRepository.get_by_id(quote_id)
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="명언을 찾을 수 없습니다",
            )

        #중복 북마크 확인
        existing = await QuoteBookmarkRepository.get_by_user_and_quote(user, quote)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 북마크 된 명언입니다",
            )

        return await QuoteBookmarkRepository.create(user, quote)

    @staticmethod
    async def get_bookmarks(user: User) -> list[QuoteBookmark]:
        return await QuoteBookmarkRepository.get_by_user(user)

    @staticmethod
    async def remove_bookmark(user: User, quote_id: int) -> None:
        quote = await QuoteRepository.get_by_id(quote_id)
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="명언을 찾을 수 없습니다",
            )

        bookmark = await QuoteBookmarkRepository.get_by_user_and_quote(user, quote)
        if not bookmark:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="명언을 찾을 수 없습니다",
            )

        await QuoteBookmarkRepository.delete(bookmark)