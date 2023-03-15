from pydantic import BaseModel, Field


class UserBaes(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserIn(UserBaes):
    key: str


class UserOut(UserBaes):
    id: int | None = Field(alias='user_id')

    class Config:
        allow_population_by_field_name = True
