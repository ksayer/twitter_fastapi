from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ValidationError
from src.db.base_class import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, **kwargs) -> Any:
        query = select(self.model).filter_by(**kwargs)  # type: ignore
        result = await db.execute(query)
        result = result.scalars().first()
        if not result:
            raise ValidationError(model_name=self.model.__tablename__)
        return result

    async def get_or_none(self, db: AsyncSession, **kwargs) -> Any:
        query = select(self.model).filter_by(**kwargs)  # type: ignore
        result = await db.execute(query)
        result = result.scalars().first()
        return result

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, **kwargs
    ):
        query = (
            select(self.model)
            .filter_by(**kwargs)  # type: ignore
            .offset(skip)
            .limit(limit)
        )
        objects = await db.execute(query)
        return objects.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        return db_obj
