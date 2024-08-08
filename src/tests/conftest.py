import asyncio
import os
import sys
from pathlib import Path

import alembic
import pytest
from alembic.config import Config
from typing import Generator
from fastapi import FastAPI
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pydantic import PostgresDsn, MySQLDsn
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from models import Base
from db import get_async_db
from config import settings

from main import app as fast_api_app


def pytest_sessionstart(session: pytest.Session):
    try:
        db_uri = MySQLDsn.build(
            scheme="mysql+pymysql",
            username=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            host=settings.MYSQL_SERVER,
            path=f"test_{settings.MYSQL_DB or ''}"

        ).__str__()
        engine = create_engine(
            db_uri, pool_pre_ping=True  # , echo=True
        )
        os.environ["TESTING"] = "1"
        if not database_exists(engine.url):
            create_database(engine.url)
        Base.metadata.create_all(bind=engine)
        # config = Config("alembic.ini")
        # try:
        #     alembic.command.revision(config, autogenerate=True)
        # except alembic.util.exc.CommandError as e:
        #     print("Alembic", e)
        # alembic.command.upgrade(config, "head")
    except Exception as e:
        raise e


@pytest_asyncio.fixture
async def db() -> AsyncSession:
    engine = create_async_engine(
        settings.SQLALCHEMY_ASYNC_DATABASE_URI.__str__().replace("lucid", 'test_lucid'))  # future=True)  # echo=True,
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)
    async with async_session() as s:
        yield s
    await engine.dispose()
    await s.close()


# fast_api_app.dependency_overrides[get_async_db] = db


@pytest.fixture(scope="session")
def app():
    yield fast_api_app


@pytest_asyncio.fixture
async def async_client(app: FastAPI,db:AsyncSession):
    async def override_get_async_db():
        yield db

    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client


def pytest_sessionfinish(session: pytest.Session, exitstatus):
    # db_uri = settings.SQLALCHEMY_ASYNC_DATABASE_URI.__str__().replace("lucid",'test_lucid')
    db_uri = MySQLDsn.build(
        scheme="mysql+pymysql",
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_SERVER,
        path=f"test_{settings.MYSQL_DB or ''}",

    ).__str__()

    engine = create_engine(db_uri, pool_pre_ping=True)
    metadata_obj = MetaData()
    for tbl in reversed(metadata_obj.sorted_tables):
        engine.execute(tbl.delete())
    drop_database(engine.url)
