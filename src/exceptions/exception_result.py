class ExceptionResult:
    """
    ExceptionResult class to define and retrieve structured error messages.

    This class contains predefined error messages for various exceptions and provides
    a method to get the appropriate content based on the exception type.
    """

    # Predefined error messages
    INTERNAL_SERVER_ERROR = {
        "status_code": 500,
        "message": "not ok",
        "result": "internal server error"
    }

    UserExistsWithThisEmail = {
        "status_code": 4044,
        "message": "not ok",
        "result": "User with this email already exists"
    }

    InvalidCredentials = {
        "status_code": 4004,
        "message": "not ok",
        "result": "Invalid credentials"
    }

    PayloadSizeExceed = {
        "status_code": 4100,
        "message": "not ok",
        "result": "Payload size exceed 1 MB"
    }

    InvalidToken = {
        "status_code": 4010,
        "message": "not ok",
        "result": "Invalid token"
    }

    InvalidTokenType = {
        "status_code": 4011,
        "message": "not ok",
        "result": "Invalid token type"
    }

    NotOwnerException = {
        "status_code": 4003,
        "message": "not ok",
        "result": "Not owner"
    }

    ItemNotFound = {
        "status_code": 4040,
        "message": "not ok",
        "result": "Item not found"
    }

    def get_content(self, exc: Exception) -> dict:
        """
        Get the structured content for the given exception.

        Args:
            exc (Exception): The exception instance.

        Returns:
            dict: The structured error message corresponding to the exception.
        """
        # Check if the class has an attribute matching the exception's class name
        if hasattr(self, exc.__class__.__name__):
            # Get the attribute (which is a predefined error message)
            exception_detail = getattr(self, exc.__class__.__name__)
            # If the attribute is callable, call it with the exception's value
            if callable(exception_detail):
                return exception_detail(exc.val)
            return exception_detail
        # Default to internal server error if no matching exception is found
        return self.INTERNAL_SERVER_ERROR

# Instantiate the ExceptionResult class to be used globally
exception_result = ExceptionResult()
