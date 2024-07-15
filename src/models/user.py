from typing import List

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, validates, Mapped
from email_validator import validate_email

from models.base import Base
from models.post import Post
from extras.security import create_token

class User(Base):
    """
    SQLAlchemy model for the 'users' table.

    Attributes:
        id (int): Primary key for the table.
        email (str): Email of the user.
        password (str): Hashed password of the user.
        posts (List[Post]): List of posts created by the user.
    """
    __tablename__ = 'users'  # Define a table name for clarity
    __allow_unmapped__ = True

    id: Mapped[int] = Column(Integer, primary_key=True)  # Primary key
    email: Mapped[str] = Column(String(100), index=True, unique=True)  # Email of the user
    password: Mapped[str] = Column(String(250))  # Hashed password of the user

    # Relationship to the Post model
    posts: Mapped[List["Post"]] = relationship('Post', uselist=True, back_populates='user', lazy='selectin')

    @validates('email')
    def validate_email(self, key: str, email: str) -> str:
        """
        Validate the email field using the email_validator library.

        Args:
            key (str): The name of the field being validated.
            email (str): The email address to validate.

        Returns:
            str: The normalized and validated email address.

        Raises:
            ValueError: If the email address is invalid.
        """
        try:
            validated_email = validate_email(email, check_deliverability=False).normalized
        except Exception as e:
            raise ValueError("Invalid email") from e
        return validated_email

    @property
    async def get_token(self) -> str:
        """
        Generate a JWT token for the user.

        Returns:
            str: The generated JWT token.
        """
        return await create_token(self)
