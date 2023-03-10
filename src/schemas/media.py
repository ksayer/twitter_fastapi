from pydantic import BaseModel


class MediaOut(BaseModel):
    id: int
    file: str

    class Config:
        orm_mode = True
