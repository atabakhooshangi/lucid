import re
from typing import Optional, List, Any
from datetime import datetime, date
from pydantic import EmailStr, Field

from pydantic import BaseModel, field_validator, model_validator

from schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserInSchema(BaseModel):
    email: EmailStr
    password: str
    re_password: str = Field(..., exclude=True)

    # @field_validator('email')
    # def check_email(cls, value):
    #     if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
    #         raise ValueError('Invalid email address')
    #     return value

    @model_validator(mode='before')
    def check_password(cls, values):
        if len(values['password']) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)', values['password']):
            raise ValueError('Password must contain at least one uppercase letter and one number')
        if values['password'] != values['re_password']:
            raise ValueError('passwords do not match')
        return values


class RegisterOut(BaseModel):
    token: str


class UserUpdate(BaseModel):
    pass
