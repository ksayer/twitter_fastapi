from pydantic import BaseModel


class TwitBase(BaseModel):
    content: str

    class Config:
        orm_mode = True


class TwitOut(TwitBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
