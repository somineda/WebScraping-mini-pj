from pydantic import BaseModel


#관리자용 질문 생성 요청
class QuestionCreate(BaseModel):
    content: str
    category: str | None = None


#질문응답
class QuestionResponse(BaseModel):
    id: int
    content: str
    category: str | None

    class Config:
        from_attributes = True