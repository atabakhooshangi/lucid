from pydantic import BaseModel
from schemas.base import BaseSchema


class PostIn(BaseModel):
    """
    Pydantic model for creating a new post.

    Attributes:
        title (str): The title of the post.
        content (str): The content of the post.
    """
    title: str
    content: str


class PostOut(BaseSchema):
    """
    Pydantic model for returning post details.

    Inherits from BaseSchema to include common timestamp fields.

    Attributes:
        id (int): The unique identifier of the post.
        title (str): The title of the post.
        content (str): The content of the post.
    """
    id: int
    title: str
    content: str

    class Config:
        """
        Pydantic configuration class.

        Enables ORM mode to allow reading data from ORM models directly.
        """
        from_attributes = True


class PostUpdate(BaseModel):
    """
    Pydantic model for updating a post.

    Currently, this model does not include any fields, but it can be expanded in the future.
    """
    pass
