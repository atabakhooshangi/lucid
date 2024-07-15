from exceptions.base_exception import BaseCustomHttpException


class PayloadSizeExceed(BaseCustomHttpException):
    """
    Exception raised when the payload size exceeds the allowed limit.

    Inherits from BaseCustomHttpException with a default status code of 400.
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(PayloadSizeExceed, self).__init__(status_code=400, val=val, *args, **kwargs)


class NotOwnerException(BaseCustomHttpException):
    """
    Exception raised when an action is attempted by a user who is not the owner of the resource.

    Inherits from BaseCustomHttpException with a default status code of 403 (Forbidden).
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(NotOwnerException, self).__init__(status_code=403, val=val, *args, **kwargs)


class ItemNotFound(BaseCustomHttpException):
    """
    Exception raised when a requested item is not found.

    Inherits from BaseCustomHttpException with a default status code of 404 (Not Found).
    """

    def __init__(self, val: str = None, *args, **kwargs):
        super(ItemNotFound, self).__init__(status_code=404, val=val, *args, **kwargs)
