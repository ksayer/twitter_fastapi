from pydantic import BaseModel, Field, validator

from src.core.config import settings
from src.schemas.user import UserOut


class TwitIn(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None = None

    class Config:
        orm_mode = True


class TwitOut(BaseModel):
    tweet_id: int
    result: bool = True

    class Config:
        orm_mode = True


class TwitOutFeed(BaseModel):
    tweet_id: int = Field(alias='id')
    tweet_data: str = Field(alias='content')
    media: list[str] | None = Field(alias='attachments')
    user: UserOut | None = Field(alias='author')
    liked_users: list[UserOut] | None = Field(alias='likes')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @validator('media', pre=True)
    def validate_media(cls, value):
        if value is not None:
            return [
                '{url}{name}'.format(url=settings.MEDIA_URL, name=media.file)
                for media in value
            ]

    @validator('liked_users', pre=True)
    def validate_liked_users(cls, value):
        if value is not None:
            return [user for user in value]
