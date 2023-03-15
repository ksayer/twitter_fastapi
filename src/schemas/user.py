from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserIn(UserBase):
    key: str


class FollowerOut(UserBase):
    id: int | None


class UserOut(UserBase):
    id: int | None = Field(alias='user_id')
    followers: list[FollowerOut] | None
    following: list[FollowerOut] | None

    class Config:
        allow_population_by_field_name = True
