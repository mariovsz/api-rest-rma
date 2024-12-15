from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from . import services
from .schemas import Permiso, RolePermiso, RolePermisoCreate, RolePermisoDelete

router = APIRouter()


@router.get(
    "/",
    response_model=list[Permiso],
    # dependencies=[Depends(permiso_requerido("read_permisos"))],
)
def read_permisos(db: Session = Depends(get_db)):
    return services.get_permisos(db)


@router.get(
    "/role/",
    response_model=list[RolePermiso],
    # dependencies=[Depends(permiso_requerido("read_role_permisos"))],
)
def read_role_permisos(db: Session = Depends(get_db)):
    return services.get_role_permisos(db)


@router.post(
    "/assign/",
    response_model=RolePermiso,
    # dependencies=[Depends(permiso_requerido("assign_role_permisos"))],
)
def assign_role_permisos(
    rolepermiso: RolePermisoCreate,
    db: Session = Depends(get_db),
):
    return services.assign_permiso_to_role(db, rolepermiso)


@router.delete(
    "/revoke/",
    response_model=RolePermisoDelete,
    # dependencies=[Depends(permiso_requerido("revoke_role_permisos"))],
)
def revoke_role_permisos(
    rolepermiso: RolePermiso,
    db: Session = Depends(get_db),
):
    return services.revoke_permiso_from_role(db, rolepermiso)
