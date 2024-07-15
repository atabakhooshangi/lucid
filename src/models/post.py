from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped
from .base import Base

class Post(Base):
    """
    SQLAlchemy model for the 'posts' table.

    Attributes:
        id (int): Primary key for the table.
        title (str): Title of the post.
        content (str): Content of the post.
        user_id (int): Foreign key to the user who created the post.
        user (relationship): Relationship to the User model.
    """
    __tablename__ = 'posts'  # Define a table name for clarity

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    title: Mapped[str] = Column(String(255), nullable=False)  # Title of the post
    content: Mapped[str] = Column(Text, nullable=False)  # Content of the post
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to user

    # Define a relationship to the User model (assuming a User model exists)
    user = relationship("User", back_populates="posts", lazy='selectin')
