import logging
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update
from fastapi import HTTPException
from sqlalchemy import delete as sqlalchemy_delete

from models import Base

# Type variables for generic CRUD operations
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Parameters:
            model (Type[ModelType]): A SQLAlchemy model class.
        """
        self.model = model

    async def async_get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID in an asynchronous session.

        Args:
            db (AsyncSession): The database session.
            id (Any): The ID of the record to retrieve.

        Returns:
            Optional[ModelType]: The retrieved record, or None if not found.
        """
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    # Additional CRUD methods can be added here

