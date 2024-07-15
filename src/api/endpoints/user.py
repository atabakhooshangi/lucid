from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from db import get_async_db

router = APIRouter()


@router.post("/register/",
             status_code=201)
async def register(
        user_in: schemas.UserInSchema,
        db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Register a new user.

    Args:
        user_in (schemas.UserInSchema): The input data for the user registration.
        db (AsyncSession): The database session dependency.

    Returns:
        Any: A dictionary containing the token for the newly registered user.
    """
    user = await crud.user.create_user(db, user_in)
    return {"token": await user.get_token}


@router.post("/login/",
             status_code=200)
async def login(
        login_schema: schemas.LoginSchema,
        db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Login an existing user.

    Args:
        login_schema (schemas.LoginSchema): The input data for user login.
        db (AsyncSession): The database session dependency.

    Returns:
        Any: A dictionary containing the token for the authenticated user.
    """
    user = await crud.user.authenticate_user(db, login_schema)
    return {"token": await user.get_token}
