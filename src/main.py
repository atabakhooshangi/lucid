from contextlib import asynccontextmanager
from api.api_router import api_router
from config import settings
from db.session import AsyncDBSingleton
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from exceptions.base_exception import (
    get_exception_handlers,
    get_validation_exception_handlers,
    get_request_validation_exception_handlers
)
from extras.response_model import CustomJSONResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.

    This function is an async context manager that performs actions during the
    startup and shutdown of the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    yield
    await AsyncDBSingleton.close()

# Initialize FastAPI app with custom lifespan and response class
app = FastAPI(
    lifespan=lifespan,
    title="lucid",
    docs_url="/docs",
    default_response_class=CustomJSONResponse
)

# Add CORS middleware if enabled in settings
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for simplicity
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

# Include the API router
app.include_router(api_router)

# Add custom exception handlers
app.add_exception_handler(*get_exception_handlers())
app.add_exception_handler(*get_validation_exception_handlers())
app.add_exception_handler(*get_request_validation_exception_handlers())

# Main entry point for running the application with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
