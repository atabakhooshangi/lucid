from exceptions.base_exception import BaseCustomHttpException


class GroupNotFound(BaseCustomHttpException):
    pass


class UserNotFoundWithReferralCode(BaseCustomHttpException):
    pass


class UserExistsWithMobile(BaseCustomHttpException):
    pass
