from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.pool import NullPool
from config import settings


class AsyncDBSingleton:
    _engine = None
    _async_session = None

    @classmethod
    async def init_engine(cls):
        """Initialize the async engine if not already done."""
        if cls._engine is None:
            cls._engine = create_async_engine(
                settings.SQLALCHEMY_ASYNC_DATABASE_URI.__str__(),
                future=True,
                poolclass=NullPool,
                pool_pre_ping=True
            )
        return cls._engine

    @classmethod
    async def get_session(cls):
        """Get the async session scoped to the current task."""
        if cls._async_session is None:
            engine = await cls.init_engine()
            cls._async_session = async_sessionmaker(
                engine, expire_on_commit=False, class_=AsyncSession, future=True
            )
        return async_scoped_session(cls._async_session, scopefunc=current_task)

    @classmethod
    async def close(cls):
        """Dispose the engine."""
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None
            cls._async_session = None


async def get_async_db() -> AsyncSession:
    """Yields a database session."""
    db_session = None
    try:
        db_session = await AsyncDBSingleton.get_session()
        yield db_session
    except Exception as e:
        print("DB Error", e)
        await db_session.rollback()
    finally:
        if db_session:
            await db_session.close()
