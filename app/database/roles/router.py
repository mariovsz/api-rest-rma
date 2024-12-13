from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from . import services
from .schemas import Role, RoleCreate, RoleUpdate, UsuarioRole, UsuarioRoleCreate


router = APIRouter()


@router.get(
    "/",
    response_model=list[Role],
    # dependencies=[Depends(permiso_requerido("read_roles"))],
)
def get_roles(db: Session = Depends(get_db)):
    return services.get_roles(db)


@router.post(
    "/",
    response_model=Role,
    # dependencies=[Depends(permiso_requerido("create_roles"))],
)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return services.create_role(db, role)


@router.put(
    "/{role_id}",
    response_model=Role,
    # dependencies=[Depends(permiso_requerido("update_roles"))],
)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return services.update_role(db, role_id, role)


@router.delete(
    "/{role_id}",
    response_model=dict,
    # dependencies=[Depends(permiso_requerido("delete_roles"))],
)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return services.delete_role(db, role_id)


@router.post(
    "/assign/",
    response_model=UsuarioRole,
    # dependencies=[Depends(permiso_requerido("assign_roles"))],
)
def assign_roles(usuario_role_data: UsuarioRoleCreate, db: Session = Depends(get_db)):
    return services.assign_role_to_user(db, usuario_role_data)


@router.delete(
    "/revoke/",
    response_model=dict,
    # dependencies=[Depends(permiso_requerido("assign_roles"))],
)
def revoke_roles(usuario_role_data: UsuarioRole, db: Session = Depends(get_db)):
    return services.revoke_role_from_user(db, usuario_role_data)
