from exceptions.base_exception import BaseCustomHttpException


class UserExistsWithThisEmail(BaseCustomHttpException):
    """
    Exception raised when a user attempts to register with an email that already exists.

    Inherits from BaseCustomHttpException with a default status code of 400 (Bad Request).
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(UserExistsWithThisEmail, self).__init__(status_code=400, val=val, *args, **kwargs)


class InvalidCredentials(BaseCustomHttpException):
    """
    Exception raised when user credentials are invalid.

    Inherits from BaseCustomHttpException with a default status code of 401 (Unauthorized).
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(InvalidCredentials, self).__init__(status_code=401, val=val, *args, **kwargs)


class InvalidToken(BaseCustomHttpException):
    """
    Exception raised when a token is invalid.

    Inherits from BaseCustomHttpException with a default status code of 401 (Unauthorized).
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(InvalidToken, self).__init__(status_code=401, val=val, *args, **kwargs)


class InvalidTokenType(BaseCustomHttpException):
    """
    Exception raised when the token type is invalid.

    Inherits from BaseCustomHttpException with a default status code of 401 (Unauthorized).
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(InvalidTokenType, self).__init__(status_code=401, val=val, *args, **kwargs)
