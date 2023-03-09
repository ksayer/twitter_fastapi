from pydantic import BaseModel, Field


class TwitIn(BaseModel):
    content: str
    tweet_media_ids: list[int] | None

    class Config:
        orm_mode = True


class TwitOut(BaseModel):
    id: int
    result: bool = True

    class Config:
        orm_mode = True
