from fastapi import APIRouter
from api.endpoints.user import router as user_router
from api.endpoints.post import router as post_router

# Create the main API router
api_router = APIRouter()

# Include the user-related endpoints with the prefix "/user" and tag "user"
api_router.include_router(user_router, prefix="/user", tags=["user"])

# Include the post-related endpoints with the prefix "/post" and tag "post"
api_router.include_router(post_router, prefix="/post", tags=["post"])
