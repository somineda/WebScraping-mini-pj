from datetime import date as date_type, datetime

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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True