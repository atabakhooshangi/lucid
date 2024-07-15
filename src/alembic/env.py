import os
import sys
from pathlib import Path
from logging.config import fileConfig

# Set the base directory to the parent of the parent directory of this file
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from config import settings
from alembic import context
from sqlalchemy import engine_from_config, pool

# Reorganize sys.path to prioritize current and parent directories
sys.path = ['', '..'] + sys.path[1:]

# Alembic Config object
config = context.config

# Configure logging from the config file
fileConfig(config.config_file_name)

from models import Base

# Metadata object from the Base class in models
target_metadata = Base.metadata

def get_url():
    """
    Construct the database URL from settings.

    Returns:
        str: The constructed database URL.
    """
    user = settings.MYSQL_USER
    password = settings.MYSQL_PASSWORD
    server = settings.MYSQL_SERVER
    db = settings.MYSQL_DB
    port = settings.MYSQL_PORT
    return f"mysql+pymysql://{user}:{password}@{server}:{port}/{db}"

def create_alembic_versions_folder():
    """
    Create the Alembic versions folder if it does not exist.

    This function checks for the existence of the 'alembic/versions'
    directory and creates it if it is missing. This ensures that
    Alembic migrations have a place to store migration scripts.
    """
    alembic_versions_path = 'alembic/versions'  # Adjust this path if your Alembic setup is located differently
    if not os.path.exists(alembic_versions_path):
        os.makedirs(alembic_versions_path)
        print(f"Created missing '{alembic_versions_path}' directory for Alembic migrations.")
    else:
        print(f"'{alembic_versions_path}' directory already exists.")

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    By skipping the Engine creation we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the script output.
    """
    create_alembic_versions_folder()
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this scenario, we need to create an Engine and associate a connection with the context.
    """
    create_alembic_versions_folder()
    DB_URL = get_url()

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DB_URL
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if the context is in offline mode or online mode and run migrations accordingly
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
