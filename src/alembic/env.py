import os
import sys
from pathlib import Path
from logging.config import fileConfig

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))
from config import settings
from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path = ['', '..'] + sys.path[1:]
# from dotenv import load_dotenv

# load_dotenv(verbose=True)
#
# env_path = Path(f'{BASE_DIR}/.env')
# load_dotenv(dotenv_path=env_path)
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

from models import Base

target_metadata = Base.metadata


# logger = logging.getLogger(__name__)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    user = settings.MYSQL_USER
    password = settings.MYSQL_PASSWORD
    server = settings.MYSQL_SERVER
    db = settings.MYSQL_DB
    port = settings.MYSQL_PORT
    return f"mysql+pymysql://{user}:{password}@{server}:{port}/{db}"


def create_alembic_versions_folder():
    alembic_versions_path = 'alembic/versions'  # Adjust this path if your Alembic setup is located differently
    if not os.path.exists(alembic_versions_path):
        os.makedirs(alembic_versions_path)
        print(f"Created missing '{alembic_versions_path}' directory for Alembic migrations.")
    else:
        print(f"'{alembic_versions_path}' directory already exists.")

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    create_alembic_versions_folder()
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

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


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
