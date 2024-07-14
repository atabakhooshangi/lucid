import json
import logging

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from schemas import UserSchema

logger = logging.getLogger(__name__)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'{settings.IAM_DOMAIN}{settings.API_V1_STR}/auth/login/access_token/' if settings.PROJECT_NAME is None \
        else f'{settings.IAM_DOMAIN}{settings.API_V1_STR}/iam/auth/login/access_token/')

JWT_ALGORITHM = "RS256"


async def get_current_user_info(
        redis_conn: aioredis = Depends(get_ioredis_connection),
        token: str = Depends(reusable_oauth2)

) -> UserSchema:
    try:
        # redis_conn = await anext(get_ioredis_connection())
        payload = jwt.decode(token, settings.USER_RSA_PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        session_data = payload['session']
        user_data = await redis_conn.get(f"user:{session_data}")
        if not user_data:
            raise Exception("session not found in redis")
        user_data = json.loads(user_data)
        return schemas.UserInfo(
            id=int(user_data["id"]),
            authentication_level=user_data["authentication_level"]
        )
    except (jwt.InvalidSignatureError, Exception) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

