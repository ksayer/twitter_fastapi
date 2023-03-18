from pydantic import BaseModel


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserIn(UserBase):
    key: str


class UserOut(UserBase):
    id: int | None


class UserOutFollowers(UserBase):
    id: int | None
    followers: list[UserOut] | None
    following: list[UserOut] | None

    class Config:
        allow_population_by_field_name = True


class UserOutFollowersResponse(BaseModel):
    result: bool = True
    user: UserOutFollowers

    class Config:
        orm_mode = True
