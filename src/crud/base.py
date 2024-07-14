import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update
from fastapi import HTTPException
from sqlalchemy import delete as sqlalchemy_delete

from models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def async_get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_or_create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(self,
                     db: AsyncSession,
                     *,
                     obj_id: int,
                     obj_in: Union[UpdateSchemaType, Dict[str, Any]]
                     ) -> ModelType:
        try:
            query = (
                sqlalchemy_update(self.model)
                .where(self.model.id == obj_id)
                .values(**obj_in.__dict__)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(query)
        except Exception as e:
            logging.info(e)
            await db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Not Found!",
            )

        await db.commit()
        obj = await self.async_get(db=db, id=obj_id)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail="Not Found!",
            )
        return obj

    async def async_remove(self, db: AsyncSession, *, id: int) -> None:
        query = sqlalchemy_delete(self.model).where(self.model.id == id)
        await db.execute(query)
        await db.commit()
        return

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
