from pydantic import BaseModel, Field


class MediaOut(BaseModel):
    id: int = Field(alias='media_id')
    file: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
