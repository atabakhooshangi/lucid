from sqlalchemy import Column, Integer, String, ForeignKey, DateTime , Text
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from .base import Base


class Post(Base):
    __tablename__ = 'posts'  # Define a table name for clarity

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    title: Mapped[str] = Column(String(255), nullable=False)  # Title of the post
    content: Mapped[str] = Column(Text, nullable=False)  # Content of the post
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)  # Creation timestamp
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to user

    # Define a relationship to the User model (assuming a User model exists)
    user = relationship("User", back_populates="posts", lazy='selectin')

