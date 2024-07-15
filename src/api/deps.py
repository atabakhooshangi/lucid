import logging
import jwt
from fastapi.requests import Request

from config import settings
from exceptions import PayloadSizeExceed, InvalidTokenType, InvalidToken
from schemas import UserSchema

# Set up logging
logger = logging.getLogger(__name__)

# Define the JWT algorithm to be used
JWT_ALGORITHM = "RS256"


async def get_current_user(request: Request) -> UserSchema:
    """
    Get the current user from the Authorization header in the request.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        UserSchema: The user schema containing the user information.

    Raises:
        InvalidTokenType: If the token type is not Bearer.
        InvalidToken: If the token is invalid or decoding fails.
    """
    try:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise InvalidToken("Authorization header missing")

        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise InvalidTokenType

        payload = jwt.decode(token, settings.USER_RSA_PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        return payload['user_id']

    except (jwt.InvalidSignatureError, Exception) as e:
        logger.error(e)
        raise InvalidToken


async def validate_content_length(request: Request):
    """
    Validate the content length of the incoming request.

    Args:
        request (Request): The incoming HTTP request.

    Raises:
        PayloadSizeExceed: If the content length exceeds the maximum allowed size.
    """
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.PAYLOAD_MAX_SIZE * 1024 * 1024:  # 1 MB limit
        raise PayloadSizeExceed
