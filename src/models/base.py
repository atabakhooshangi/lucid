import datetime
from typing import Any
from sqlalchemy import DateTime, Column, Integer
from sqlalchemy.orm import as_declarative, declared_attr

class TimestampMixin:
    """
    Mixin class to add timestamp columns to a SQLAlchemy model.

    Attributes:
        created_at (DateTime): The date and time when the record was created.
        updated_at (DateTime): The date and time when the record was last updated.
    """
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), onupdate=datetime.datetime.now)

@as_declarative()
class Base(TimestampMixin):
    """
    Base class for all SQLAlchemy models, incorporating timestamp columns and
    automatic table name generation.

    Attributes:
        id (Integer): The primary key for the table.
        __name__ (str): The name of the class, used to generate the table name.
        __allow_unmapped__ (bool): Allow unmapped columns in the model.
    """
    id: Any = Column(Integer, primary_key=True, index=True)
    __name__: str
    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically using the class name.

        Returns:
            str: The generated table name, which is the lowercase version of the class name.
        """
        return cls.__name__.lower()
