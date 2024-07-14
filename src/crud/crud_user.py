from datetime import datetime
from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, load_only, joinedload, noload
from sqlalchemy.sql.elements import or_
from starlette import status

import schemas
from crud.base import CRUDBase
from exceptions import UserExistsWithThisEmail
from models import User
from extras.security import get_password_hash


class CRUDUser(CRUDBase[User, schemas.UserInSchema, schemas.UserUpdate]):

    async def get_user(self, db: AsyncSession, *, user_id: int) -> Optional[User]:
        query = await db.execute(
            select(User).options(
                load_only(User.id, User.email),
                noload(User.posts)
            ).filter(User.id == user_id)
        )
        user = query.scalar()
        return user

    async def create_user(self, db: AsyncSession, user_in: schemas.UserInSchema) -> User:
        # user_in_data = jsonable_encoder(user_in)

        hashed_pass = get_password_hash(user_in.password)
        user_in.password = hashed_pass
        user = User(**user_in.model_dump())
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError:
            raise UserExistsWithThisEmail


user = CRUDUser(User)
