from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import Role, UsuarioRole
from .schemas import (
    RoleCreate,
    RoleUpdate,
    RoleDelete,
    UsuarioRoleCreate,
    UsuarioRoleDelete,
)
from .schemas import Role as RoleSchema, UsuarioRole as UsuarioRoleSchema
from ..users.services import get_user_or_404


def get_role_or_404(db: Session, role_id: int) -> Role:
    role = Role.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role


def get_roles(db: Session) -> list[RoleSchema]:
    roles = Role.filter(db, is_active=True)
    return [RoleSchema.model_validate(role) for role in roles]


def create_role(db: Session, role: RoleCreate) -> RoleSchema:
    new_role = Role.create(db, role)
    return RoleSchema.model_validate(new_role)


def update_role(db: Session, role_id: int, updated_role: RoleUpdate) -> RoleSchema:
    role = get_role_or_404(db, role_id)
    role.update(db, updated_role)
    return RoleSchema.model_validate(role)


def delete_role(db: Session, role_id: int) -> RoleDelete:
    role = get_role_or_404(db, role_id)
    role.delete(db)
    return RoleDelete(detail=f"Rol {role} eliminado correctamente")


def get_user_roles(db: Session) -> list[UsuarioRoleSchema]:
    userroles = UsuarioRole.filter(db)
    return [UsuarioRoleSchema.model_validate(userrole) for userrole in userroles]


def assign_role_to_user(
    db: Session,
    userrole: UsuarioRoleCreate,
) -> UsuarioRoleSchema:
    user = get_user_or_404(db, userrole.usuario_id)
    role = get_role_or_404(db, userrole.role_id)
    existing_relation = UsuarioRole.find_first(
        db,
        usuario_id=user.id,
        role_id=role.id,
    )
    if not existing_relation:
        UsuarioRole.create(db, userrole)
    return UsuarioRoleSchema.model_validate(userrole)


def revoke_role_from_user(
    db: Session, userrole: UsuarioRoleSchema
) -> UsuarioRoleDelete:
    existing_relation = UsuarioRole.find_first(
        db,
        usuario_id=userrole.usuario_id,
        role_id=userrole.role_id,
    )
    if not existing_relation:
        raise HTTPException(
            status_code=404, detail="Relación de usuario y rol no encontrada"
        )
    existing_relation.delete(db)
    return UsuarioRoleDelete(detail="Rol revocado del Usuario")
