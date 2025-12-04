from datetime import date

from pydantic import BaseModel

class DiaryCreate(BaseModel):
    title: str
    content: str
    date: date

class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    date: date | None = None

class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    date: date
    user_id: int

    class Config:
        from_attributes = True