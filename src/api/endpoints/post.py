from typing import Any
from fastapi import APIRouter, Depends

import schemas
from api.deps import get_current_user, validate_content_length
from crud.in_memory import save_post, response_cache, get_cached_posts, delete_in_mem_post
from exceptions import ItemNotFound

router = APIRouter()


@router.post("/",
             status_code=201)
async def create_post(
        post_in: schemas.PostIn,
        # db: AsyncSession = Depends(get_async_db),
        user_id: int = Depends(get_current_user),
        _=Depends(validate_content_length)

) -> int:
    """
        Create a new post.

        Args:
            post_in (schemas.PostIn): The input data for the post.
            user_id (int): The ID of the current user, obtained from dependencies.
            _ : Placeholder for content length validation.

        Returns:
            int: The ID of the newly created post.
        """

    # Save post to in-memory storage
    post_id = save_post(str(user_id), post_in.content)

    # Uncomment the following lines to use database interaction:
    # db: AsyncSession = Depends(get_async_db) should be added to the function signature.
    # post = await crud.post.create_post(db, post_in, user_id)
    # return post
    return post_id


@router.get("/",
            # response_model=List[schemas.PostOut],
            status_code=200)
async def get_posts(
        # db: AsyncSession = Depends(get_async_db),
        user_id: int = Depends(get_current_user)
) -> list:
    """
        Get all posts for the current user.

        Args:
            user_id (int): The ID of the current user, obtained from dependencies.

        Returns:
            list: The list of posts for the current user.
        """

    # Get posts from in-memory cache
    user_posts = get_cached_posts(str(user_id))
    response_cache[user_id] = user_posts

    # Uncomment the following lines to use database interaction:
    # db: AsyncSession = Depends(get_async_db) should be added to the function signature.
    # posts = await crud.post.get_user_posts(db, user_id)
    # return posts

    return user_posts


@router.delete("/{post_id}/")
async def delete_post(
        post_id: int,
        # db: AsyncSession = Depends(get_async_db),
        user_id: int = Depends(get_current_user)
) -> Any:
    """
        Delete a post by ID.

        Args:
            post_id (int): The ID of the post to delete.
            user_id (int): The ID of the current user, obtained from dependencies.

        Returns:
            Any: None if the deletion is successful.
        """

    # Delete post from in-memory storage
    if not delete_in_mem_post(str(user_id), post_id):
        raise ItemNotFound
    return

    # Uncomment the following lines to use database interaction:
    # db: AsyncSession = Depends(get_async_db) should be added to the function signature.
    # await crud.post.async_remove_if_owner(db, id=post_id, user_id=user_id)
    # return
