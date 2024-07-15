from typing import Optional, Union
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import noload

import schemas
from crud.base import CRUDBase
from exceptions import UserExistsWithThisEmail, InvalidCredentials
from models import User
from extras.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, schemas.UserInSchema, schemas.UserUpdate]):
    """
    CRUD operations for the User model.
    """

    async def get_user(self, db: AsyncSession, *, input: Union[int, EmailStr]) -> Optional[User]:
        """
        Retrieve a user by ID or email.

        Args:
            db (AsyncSession): The database session.
            input (Union[int, EmailStr]): The user ID or email.

        Returns:
            Optional[User]: The retrieved user or None if not found.
        """
        if isinstance(input, int):
            filters = [User.id == input]
        else:
            filters = [User.email == input]
        query = await db.execute(
            select(User).options(
                noload(User.posts)  # Do not load related posts
            ).filter(*filters)
        )
        user = query.scalars().first()
        return user

    async def create_user(self, db: AsyncSession, user_in: schemas.UserInSchema) -> User:
        """
        Create a new user.

        Args:
            db (AsyncSession): The database session.
            user_in (schemas.UserInSchema): The input schema for creating a user.

        Returns:
            User: The newly created user.

        Raises:
            UserExistsWithThisEmail: If a user with the given email already exists.
        """
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

    async def authenticate_user(self, db: AsyncSession, login_schema: schemas.LoginSchema) -> Optional[User]:
        """
        Authenticate a user.

        Args:
            db (AsyncSession): The database session.
            login_schema (schemas.LoginSchema): The login schema containing user credentials.

        Returns:
            Optional[User]: The authenticated user.

        Raises:
            InvalidCredentials: If the credentials are invalid.
        """
        user = await self.get_user(db, input=login_schema.email)
        if not user:
            raise InvalidCredentials
        verify = await verify_password(login_schema.password, user.password)
        if verify:
            return user
        raise InvalidCredentials


# Instantiate the CRUDUser class for the User model
user = CRUDUser(User)
