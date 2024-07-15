from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.

    Attributes:
        created_at (Optional[datetime]): The timestamp when the record was created.
        updated_at (Optional[datetime]): The timestamp when the record was last updated.
    """
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
