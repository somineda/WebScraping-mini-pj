from datetime import date as date_type

from pydantic import BaseModel


class DiaryCreate(BaseModel):
    title: str
    content: str
    date: date_type


class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    date: date_type | None = None


class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    date: date_type
    user_id: int

    class Config:
        from_attributes = True