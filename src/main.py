from contextlib import asynccontextmanager
from api.api_router import api_router
from config import settings
from db.session import AsyncDBSingleton
from random import randint
# from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from exceptions.base_exception import get_exception_handlers, get_validation_exception_handlers, \
    get_request_validation_exception_handlers
from extras.response_model import CustomJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    await AsyncDBSingleton.close()


app = FastAPI(
    lifespan=lifespan,
    title="lucid",
    docs_url="/docs",
    default_response_class=CustomJSONResponse)

# app.add_middleware(
#     SessionMiddleware,
#     secret_key=f"{randint(1000, 4000)}-secret-string-{randint(1000, 4000)}",
#
# )

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

app.add_exception_handler(*get_exception_handlers())
app.add_exception_handler(*get_validation_exception_handlers())
app.add_exception_handler(*get_request_validation_exception_handlers())
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
