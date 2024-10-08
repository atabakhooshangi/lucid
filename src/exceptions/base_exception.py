from typing import Union, Any

from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette.requests import Request
from fastapi.responses import ORJSONResponse

from exceptions.exception_result import exception_result


class BaseCustomHttpException(HTTPException):
    """
    Base class for custom HTTP exceptions.

    Inherits from FastAPI's HTTPException and adds a `val` attribute for custom messages.
    """

    def __init__(self, status_code: int = 400, val: str = None, *args, **kwargs):
        self.val = val
        super(BaseCustomHttpException, self).__init__(status_code, *args, **kwargs)


def get_exception_handlers() -> Union[Exception, Any]:
    """
    Returns the internal exception handler.

    Returns:
        Union[Exception, Any]: The internal exception handler function.
    """
    return Union[Exception], Union[internal_exception_handler]


def get_validation_exception_handlers() -> Union[BaseCustomHttpException, Any]:
    """
    Returns the API exception handler for validation errors.

    Returns:
        Union[BaseCustomHttpException, Any]: The API exception handler function.
    """
    return BaseCustomHttpException, api_exception_handler


def get_request_validation_exception_handlers() -> Union[RequestValidationError, Any]:
    """
    Returns the API validation exception handler for request validation errors.

    Returns:
        Union[RequestValidationError, Any]: The API validation exception handler function.
    """
    return RequestValidationError, api_validation_exception_handler


def internal_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    """
    Handles internal exceptions and returns an appropriate response.

    Args:
        request (Request): The incoming request.
        exc (Exception): The exception that occurred.

    Returns:
        ORJSONResponse: The response with the appropriate status code and content.
    """
    if isinstance(exc, BaseCustomHttpException):
        return api_exception_handler(request, exc)

    if isinstance(exc, ValidationError):
        return api_validation_exception_handler(request, exc)

    return ORJSONResponse(
        status_code=500,
        content=exception_result.get_content(exc)
    )


def api_exception_handler(request: Request, exc: BaseCustomHttpException) -> ORJSONResponse:
    """
    Handles API exceptions and returns an appropriate response.

    Args:
        request (Request): The incoming request.
        exc (BaseCustomHttpException): The custom HTTP exception that occurred.

    Returns:
        ORJSONResponse: The response with the appropriate status code and content.
    """
    if isinstance(exc.detail, dict):
        return ORJSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exception_result.get_content(exc)
    )


def api_validation_exception_handler(request: Request, exc: Any) -> ORJSONResponse:
    """
    Handles API validation exceptions and returns an appropriate response.

    Args:
        request (Request): The incoming request.
        exc (Any): The validation exception that occurred.

    Returns:
        ORJSONResponse: The response with the appropriate status code and content.
    """
    result = ""
    if isinstance(exc.errors(), list):
        result = list(map(lambda error: {
            "field": error["loc"][-1],
            "detail": error["msg"]
        }, exc.errors()))

    return ORJSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "message": "not ok",
            "result": result
        }
    )
