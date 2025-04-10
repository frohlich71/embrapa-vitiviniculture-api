from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context
from app.core.config import settings
from app.db.session import engine
from app.models import production  # noqa: F401 - force model registration

# this is the Alembic Config object
config = context.config

# Set the database URL dynamically from your settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configure loggers
fileConfig(config.config_file_name)

# Set metadata for autogenerate
target_metadata = SQLModel.metadata

def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()
