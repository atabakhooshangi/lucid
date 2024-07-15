import re
from pydantic import EmailStr, Field, BaseModel, model_validator

from schemas.base import BaseSchema


class UserSchema(BaseSchema):
    """
    Pydantic model for returning user details.

    Inherits from BaseSchema to include common timestamp fields.

    Attributes:
        id (int): The unique identifier of the user.
        email (EmailStr): The email address of the user.
    """
    id: int
    email: EmailStr

    class Config:
        """
        Pydantic configuration class.

        Enables ORM mode to allow reading data from ORM models directly.
        """
        from_attributes = True


class UserInSchema(BaseModel):
    """
    Pydantic model for user registration input.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password of the user.
        re_password (str): The password confirmation (must match `password`).
    """
    email: EmailStr
    password: str
    re_password: str = Field(..., exclude=True)

    @model_validator(mode='before')
    def check_password(cls, values):
        """
        Validate the password fields.

        Ensures that the password is at least 6 characters long, contains at least one uppercase letter and one number,
        and matches the `re_password` field.

        Args:
            values (dict): The input values to validate.

        Returns:
            dict: The validated input values.

        Raises:
            ValueError: If any of the validation checks fail.
        """
        if len(values['password']) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)', values['password']):
            raise ValueError('Password must contain at least one uppercase letter and one number')
        if values['password'] != values['re_password']:
            raise ValueError('Passwords do not match')
        return values


class RegisterOut(BaseModel):
    """
    Pydantic model for the registration output.

    Attributes:
        token (str): The JWT token generated for the user.
    """
    token: str


class UserUpdate(BaseModel):
    """
    Pydantic model for updating user details.

    Currently, this model does not include any fields, but it can be expanded in the future.
    """
    pass


class LoginSchema(BaseModel):
    """
    Pydantic model for user login input.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password of the user.
    """
    email: EmailStr
    password: str
