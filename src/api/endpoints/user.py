import logging
from typing import Any, List, Union, Dict
from fastapi import APIRouter, Depends
from starlette.datastructures import QueryParams
# from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
import crud
import schemas
from db import get_async_db
from exceptions import UserExistsWithThisEmail

router = APIRouter()


@router.post("/register/",
             status_code=201)
async def register(
        user_in: schemas.UserInSchema,
        db: AsyncSession = Depends(get_async_db)
) -> Any:
    user = await crud.user.create_user(db, user_in)
    return {"token": await user.get_token}

# TODO: Add login endpoint
