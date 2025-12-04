from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


#유저
class User(BaseModel):
    email = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=100)
    password = fields.CharField(max_length=255)  
    is_active = fields.BooleanField(default=True)

   
    diaries: fields.ReverseRelation["Diary"]
    bookmarks: fields.ReverseRelation["QuoteBookmark"]

    class Meta:
        table = "users"


#JWT 블랙리스트 (로그아웃된 토큰)
class TokenBlacklist(BaseModel):
    token = fields.TextField()
    expires_at = fields.DatetimeField()

    class Meta:
        table = "token_blacklist"


#일기
class Diary(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="diaries", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    date = fields.DateField()

    class Meta:
        table = "diaries"


#명언
class Quote(BaseModel):
    content = fields.TextField()
    author = fields.CharField(max_length=100, null=True)

    bookmarks: fields.ReverseRelation["QuoteBookmark"]

    class Meta:
        table = "quotes"


#명언 북마크
class QuoteBookmark(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="bookmarks", on_delete=fields.CASCADE)
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarks", on_delete=fields.CASCADE)

    class Meta:
        table = "quote_bookmarks"
        unique_together = (("user", "quote"),) 


#오늘의 질문
class DailyQuestion(BaseModel):
    content = fields.TextField()
    category = fields.CharField(max_length=50, null=True)  

    class Meta:
        table = "daily_questions"