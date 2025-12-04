import random

from app.models import Quote, QuoteBookmark, User


class QuoteRepository:
    @staticmethod
    async def get_random() -> Quote | None:
        quotes = await Quote.all()
        if not quotes:
            return None
        return random.choice(quotes)

    @staticmethod
    async def get_by_id(quote_id: int) -> Quote | None:
        return await Quote.filter(id=quote_id).first()

    @staticmethod
    async def get_all() -> list[Quote]:
        return await Quote.all()


class QuoteBookmarkRepository:
    @staticmethod
    async def get_by_user_and_quote(user: User, quote: Quote) -> QuoteBookmark | None:
        return await QuoteBookmark.filter(user=user, quote=quote).first()

    @staticmethod
    async def get_by_user(user: User) -> list[QuoteBookmark]:
        return await QuoteBookmark.filter(user=user).prefetch_related("quote")

    @staticmethod
    async def create(user: User, quote: Quote) -> QuoteBookmark:
        return await QuoteBookmark.create(user=user, quote=quote)

    @staticmethod
    async def delete(bookmark: QuoteBookmark) -> None:
        await bookmark.delete()