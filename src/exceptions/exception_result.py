class ExceptionResult:
    INTERNAL_SERVER_ERROR = {
        "status_code": 500,
        "message": "not ok",
        "result": "internal server error"
    }

    UserExistsWithThisEmail = {
        "status_code": 4003,
        "message": "not ok",
        "result": "User with this email already exists"
    }

    IamApiGateWayException = {
        "status_code": 5001,
        "message": "not ok",
        "result": "iam service is not available"
    }

    def get_content(self, exc):
        if hasattr(self, str(exc.__class__.__name__)):
            clas = getattr(self, str(exc.__class__.__name__))
            if callable(clas):
                return clas(exc.val)
            return clas
        # print(exc.__class__.__name__)
        return self.INTERNAL_SERVER_ERROR


exception_result = ExceptionResult()
