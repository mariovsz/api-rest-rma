from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Permiso, RolePermiso
from .schemas import PermisoCreate, RolePermisoCreate, RolePermisoDelete
from .schemas import Permiso as PermisoSchema, RolePermiso as RolePermisoSchema
from ..roles.services import get_role_or_404


def get_permiso_or_404(db: Session, permiso_id: int) -> Permiso:
    permiso = Permiso.get(db, permiso_id)
    if not permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso


def create_permiso(db: Session, permiso: PermisoCreate) -> PermisoSchema:
    new_permiso = Permiso.create(db, permiso)
    return PermisoSchema.model_validate(new_permiso)


def get_permisos(db: Session) -> list[PermisoSchema]:
    permisos = Permiso.get_all(db)
    return [PermisoSchema.model_validate(permiso) for permiso in permisos]


def get_role_permisos(db: Session) -> list[RolePermisoSchema]:
    rolepermisos = RolePermiso.get_all(db)
    return [
        RolePermisoSchema.model_validate(rolepermiso) for rolepermiso in rolepermisos
    ]


def assign_permiso_to_role(
    db: Session,
    rolepermiso: RolePermisoCreate,
) -> RolePermisoSchema:
    permiso = get_permiso_or_404(db, rolepermiso.permiso_id)
    role = get_role_or_404(db, rolepermiso.role_id)
    existing_relation = RolePermiso.find_first(
        db,
        role_id=role.id,
        permiso_id=permiso.id,
    )
    if not existing_relation:
        RolePermiso.create(db, rolepermiso)
    return RolePermisoSchema.model_validate(rolepermiso)


def revoke_permiso_from_role(
    db: Session,
    rolepermiso: RolePermisoSchema,
) -> RolePermisoDelete:
    existing_relation = RolePermiso.find_first(
        db,
        role_id=rolepermiso.role_id,
        permiso_id=rolepermiso.permiso_id,
    )
    if not existing_relation:
        raise HTTPException(
            status_code=404, detail="Relación de rol y permiso no encontrada"
        )
    existing_relation.delete(db)
    return RolePermisoDelete(detail="Permiso revocado del rol")
