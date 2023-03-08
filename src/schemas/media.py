from pydantic import BaseModel


class MediaOut(BaseModel):
    file: str
    id: int

    class Config:
        orm_mode = True
