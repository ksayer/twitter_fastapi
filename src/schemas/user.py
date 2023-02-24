from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    key: str

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
