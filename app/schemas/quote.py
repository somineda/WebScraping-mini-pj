from pydantic import BaseModel

#관리자용 명언 생성
class QuoteCreate(BaseModel):
    content: str
    author: str | None = None


class QuoteResponse(BaseModel):
    id: int
    content: str
    author: str | None

    class Config:
        from_attributes = True


class QuoteBookmarkResponse(BaseModel):
    id: int
    quote: QuoteResponse

    class Config:
        from_attributes = True