from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy import pool
from dotenv import load_dotenv

import os

load_dotenv()

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL missing")


SYNC_DATABASE_URL = (
    DATABASE_URL
    .replace(
        "postgresql+asyncpg",
        "postgresql+psycopg"
    )
)

from app.models.base_model import Base
from app.db.base import *

target_metadata = Base.metadata


def run_migrations_offline():

    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True
    )

    with context.begin_transaction():

        context.run_migrations()


def run_migrations_online():

    connectable = create_engine(
        SYNC_DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():

            context.run_migrations()


if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()