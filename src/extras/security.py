import logging
import bcrypt
from datetime import datetime, timedelta

import jwt

from config import settings


logger = logging.getLogger(__name__)

ALGORITHM = "RS256"


async def create_token(
        user,
        expires_delta: timedelta = None

) -> dict:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "user_id": user.id}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.USER_RSA_PRIVATE_KEY,  # sign with rsa private key
        algorithm=ALGORITHM,
    )

    return encoded_jwt


async def verify_token(token: str):
    try:

        key = settings.USER_RSA_PUBLIC_KEY
        payload = jwt.decode(token, key, algorithms=[ALGORITHM])

        return dict(verified=True, user_data=payload)
    except Exception as e:
        logger.info(e)
        return dict(verified=False, user_data=None)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
