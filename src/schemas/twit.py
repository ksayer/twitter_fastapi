from pydantic import BaseModel


class TwitBase(BaseModel):
    content: str
    tweet_media_ids: list[int] | None

    class Config:
        orm_mode = True


class TwitOut(TwitBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
