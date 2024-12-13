from alembic import op
import sqlalchemy as sa

revision = "e8105b33fb1d"
down_revision = "e685290144f5"
branch_labels = None
depends_on = None


def upgrade():
    # Eliminar restricciones de clave foránea primero
    op.drop_constraint(
        "paquetes_archivo_type_id_fkey", "paquetes_archivo", type_="foreignkey"
    )
    op.drop_constraint("paquetes_type_id_fkey", "paquetes", type_="foreignkey")

    # Luego, eliminar índices y tablas
    op.drop_index("ix_tipos_data_type", table_name="tipos")
    op.drop_index("ix_paquetes_data", table_name="paquetes")
    op.drop_index("ix_paquetes_date", table_name="paquetes")
    op.drop_index("ix_paquetes_id", table_name="paquetes")

    op.drop_table("tipos")
    op.drop_table("paquetes")
    op.drop_table("paquetes_archivo")
    # op.create_table(
    #     "nueva_tabla",  # Nombre de la nueva tabla
    #     sa.Column("id", sa.Integer, primary_key=True),
    # )
    # Crear nuevos índices y relaciones si es necesario
    op.create_index("ix_nueva_tabla_id", "nueva_tabla", ["id"])


def downgrade():
    # Crear las tablas y los índices nuevamente en caso de reversión
    op.create_table(
        "paquetes",
        sa.Column("id", sa.Integer, primary_key=True),
        # Más columnas aquí
    )
    op.create_index("ix_paquetes_data", "paquetes", ["data"])
    op.create_index("ix_paquetes_date", "paquetes", ["date"])
    op.create_index("ix_paquetes_id", "paquetes", ["id"])

    op.create_table(
        "paquetes_archivo",
        sa.Column("id", sa.Integer, primary_key=True),
        # Más columnas aquí
    )
    op.create_index("ix_paquetes_archivo_data", "paquetes_archivo", ["data"])
    op.create_index("ix_paquetes_archivo_date", "paquetes_archivo", ["date"])
    op.create_index("ix_paquetes_archivo_id", "paquetes_archivo", ["id"])

    op.create_table(
        "tipos",
        sa.Column("id", sa.Integer, primary_key=True),
        # Más columnas aquí
    )
    op.create_index("ix_tipos_data_type", "tipos", ["data_type"])

    # Restaurar restricciones de clave foránea
    op.create_foreign_key(
        "paquetes_archivo_type_id_fkey",
        "paquetes_archivo",
        "tipos",
        ["type_id"],
        ["id"],
    )
    op.create_foreign_key(
        "paquetes_type_id_fkey", "paquetes", "tipos", ["type_id"], ["id"]
    )
