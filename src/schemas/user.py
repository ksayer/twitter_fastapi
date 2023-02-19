from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    key: str

    class Config:
        orm_mode = True
