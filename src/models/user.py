from typing import List

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, validates, Mapped
from email_validator import validate_email
from models.base import Base
from models.post import Post
from extras.security import create_token


class User(Base):
    __tablename__ = 'users'  # Define a table name for clarity
    __allow_unmapped__ = True
    id: Mapped[int] = Column(Integer, primary_key=True)  # Assuming there's an ID column
    email: Mapped[str] = Column(String(100), index=True, unique=True)
    password: Mapped[str] = Column(String(250))
    posts: Mapped[List["Post"]] = relationship('Post', uselist=True, back_populates='user', lazy='selectin')

    @validates('email')
    def validate_email(self, key, email):
        try:
            validated_email = validate_email(email, check_deliverability=False).normalized
        except Exception as e:
            raise ValueError("Invalid email") from e
        return validated_email

    @property
    async def get_token(self):
        return await create_token(self)
