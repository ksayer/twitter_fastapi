from pydantic import BaseModel


class TwitIn(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None

    class Config:
        orm_mode = True


class TwitOut(BaseModel):
    tweet_id: int
    result: bool = True

    class Config:
        orm_mode = True
