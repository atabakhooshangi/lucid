from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.pool import NullPool
from config import settings


class AsyncDBSingleton:
    """
    Singleton class to manage the asynchronous database engine and session.

    This class ensures that only one instance of the database engine and session maker
    is created and used throughout the application. It uses SQLAlchemy's async capabilities
    to manage connections and sessions for the database.
    """

    _engine = None
    _async_session = None

    @classmethod
    async def init_engine(cls):
        """
        Initialize the asynchronous database engine if it has not been initialized.

        This method creates an asynchronous engine using the connection URI from the settings.
        The engine is configured to use the `NullPool` class, meaning no connection pooling
        is done, and connections are created and closed with each request.

        Returns:
            AsyncEngine: The initialized asynchronous engine.
        """
        print(settings.SQLALCHEMY_ASYNC_DATABASE_URI.__str__())
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
        """
        Get the asynchronous session scoped to the current task.

        This method initializes the session maker if it has not been initialized and
        returns a session that is scoped to the current task. This ensures that each
        asynchronous task gets its own session.

        Returns:
            AsyncSession: The scoped asynchronous session.
        """
        if cls._async_session is None:
            engine = await cls.init_engine()
            cls._async_session = async_sessionmaker(
                engine, expire_on_commit=False, class_=AsyncSession, future=True
            )
        return async_scoped_session(cls._async_session, scopefunc=current_task)

    @classmethod
    async def close(cls):
        """
        Dispose of the database engine and session maker.

        This method disposes of the database engine and sets the engine and session maker
        attributes to None. This can be used to clean up resources when the application
        is shutting down or when the database connection needs to be reset.
        """
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None
            cls._async_session = None


async def get_async_db() -> AsyncSession:
    """
    Dependency function to provide a database session to FastAPI endpoints.

    This function yields a database session that is scoped to the current task. It handles
    the creation, commitment, and rollback of transactions, ensuring that the session is
    properly closed after each use.

    Yields:
        AsyncSession: The scoped asynchronous session.

    Raises:
        Exception: If an error occurs, the transaction is rolled back, and the exception is logged.
    """
    print('maaaaaaaaaaaaaal')
    db_session = None
    try:
        # Get a session scoped to the current task
        db_session = await AsyncDBSingleton.get_session()
        yield db_session
    except Exception as e:
        # Log the exception and rollback the transaction in case of an error
        print("DB Error", e)
        if db_session:
            await db_session.rollback()
    finally:
        # Close the session to release the resources
        if db_session:
            await db_session.close()
