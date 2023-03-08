from pydantic import BaseModel


class MediaIn(BaseModel):
    id: int = None

    class Config:
        orm_mode = True


class MediaOut(MediaIn):
    file: str

    class Config:
        orm_mode = True
