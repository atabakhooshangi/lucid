from cachetools import TTLCache
from typing import Dict, List

from config import settings

# In-memory storage for posts
posts: Dict[str, Dict[int, str]] = {}
post_id_counter = 0

# Cache for storing responses for settings.CACHE_TIME seconds
response_cache = TTLCache(maxsize=100, ttl=settings.CACHE_TIME)


def save_post(user_id: str, text: str) -> int:
    """
    Save a new post in memory.

    Args:
        user_id (str): The ID of the user creating the post.
        text (str): The content of the post.

    Returns:
        int: The ID of the newly created post.
    """
    global post_id_counter
    post_id_counter += 1
    if user_id not in posts:
        posts[user_id] = {}
    posts[user_id][post_id_counter] = text
    return post_id_counter


def get_cached_posts(user_id: str) -> List[str]:
    """
    Retrieve all cached posts for a specific user.

    Args:
        user_id (str): The ID of the user whose posts are to be retrieved.

    Returns:
        List[str]: A list of posts for the user.
    """
    return list(posts.get(user_id, {}).values())


def delete_in_mem_post(user_id: str, post_id: int) -> bool:
    """
    Delete a post from memory if it exists.

    Args:
        user_id (str): The ID of the user who owns the post.
        post_id (int): The ID of the post to be deleted.

    Returns:
        bool: True if the post was deleted, False otherwise.
    """
    if user_id in posts and post_id in posts[user_id]:
        del posts[user_id][post_id]
        return True
    return False
