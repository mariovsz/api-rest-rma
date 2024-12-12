import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool


from app.database.basemodel import ModeloBase
from app.database.nodos.models import Nodo


config = context.config
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno y establecerlas en el contexto de configuración de Alembic
config.set_main_option("POSTGRES_USER", os.getenv("POSTGRES_USER", ""))
config.set_main_option("POSTGRES_PASSWORD", os.getenv("POSTGRES_PASSWORD", ""))
config.set_main_option("POSTGRES_DB", os.getenv("POSTGRES_DB", ""))
config.set_main_option("POSTGRES_HOST", os.getenv("POSTGRES_HOST", "localhost"))
config.set_main_option("POSTGRES_PORT", os.getenv("POSTGRES_PORT", "5432"))

# Configuración del logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaDatos de los modelos
target_metadata = ModeloBase.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
