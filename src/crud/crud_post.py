from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete as sqlalchemy_delete

import schemas
from crud.base import CRUDBase
from exceptions import NotOwnerException, ItemNotFound
from models import Post


class CRUDPost(CRUDBase[Post, schemas.PostIn, schemas.PostUpdate]):
    """
    CRUD operations for the Post model.
    """

    async def create_post(self, db: AsyncSession, post_in: schemas.PostIn, user_id: int) -> Post:
        """
        Create a new post.

        Args:
            db (AsyncSession): The database session.
            post_in (schemas.PostIn): The input schema for creating a post.
            user_id (int): The ID of the user creating the post.

        Returns:
            Post: The newly created post.
        """
        post = Post(**post_in.model_dump())
        db.add(post)
        post.user_id = user_id
        await db.commit()
        await db.refresh(post)
        return post

    async def get_user_posts(self, db: AsyncSession, user_id: int) -> List[Post]:
        """
        Get all posts by a specific user.

        Args:
            db (AsyncSession): The database session.
            user_id (int): The ID of the user whose posts are to be retrieved.

        Returns:
            List[Post]: A list of posts by the user.
        """
        result = await db.execute(select(Post).filter(Post.user_id == user_id))
        return result.scalars().all()

    async def async_remove_if_owner(self, db: AsyncSession, *, id: int, user_id: int) -> None:
        """
        Remove a post if the current user is the owner.

        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the post to be removed.
            user_id (int): The ID of the user attempting to remove the post.

        Raises:
            ItemNotFound: If the post does not exist.
            NotOwnerException: If the user is not the owner of the post.
        """
        post = await self.async_get(db, id)
        if not post:
            raise ItemNotFound
        if post.user_id != user_id:
            raise NotOwnerException
        query = sqlalchemy_delete(self.model).where(self.model.id == id, self.model.user_id == user_id)
        await db.execute(query)
        await db.commit()
        return


# Instantiate the CRUDPost class for the Post model
post = CRUDPost(Post)
