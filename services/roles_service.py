from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException

from model.roles import CreateRoleRequestBody, Role, RoleResponseBody
from database.firebase import ref_roles


def get_all_roles():
    roles = ref_roles.get()

    if not roles:
        return []
    
    return [
        {
            "id": id,
            "name": role['name'],
            "description": role['description'],
            "created_at": role['created_at'],
            "updated_at": role['updated_at']
        }
        for id, role in roles.items()
    ]

def create_role(new_role: CreateRoleRequestBody):
    name, description = validate_role_data(new_role)
    timestamp = datetime.now()
    new_role = Role(
        name=name,
        description=description,
        created_at=timestamp,
        updated_at=timestamp
    )
    
    id = ref_roles.push(new_role.to_json())

    return {
        "message": "Role criada com sucesso",
        "id": id.key,
        "role": new_role.to_json()
    }

def update_role(id, new_role: CreateRoleRequestBody):
    role_exist = get_role_by_id(id)
    name, description = validate_role_data(new_role)
    
    role = Role(
        name=name,
        description=description,
        created_at=role_exist.created_at,
        updated_at=datetime.now())

    ref_roles.child(id).update(role.to_json())

    return {
        "message": "Role atualizada com sucesso",
        "id": id,
        "role": role.to_json()
    }

def delete_role(id):
    role = get_role_by_id(id)
    ref_roles.child(id).delete()
    return {
        "message": "Role deletada com sucesso"
    }

def get_role_by_id(id):
    role_found = ref_roles.child(id).get()

    if role_found:
        role = RoleResponseBody (
            id=id,
            name=role_found['name'],
            description=role_found['description'],
            created_at=role_found['created_at'],
            updated_at=role_found['updated_at'])
        return role
    
    raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado")

def validate_role_data(role: CreateRoleRequestBody):
    if len(role.name) < 3:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O nome da role deve conter pelo menos 3 caracteres")
    
    if len(role.description) < 3:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A descrição da role deve conter pelo menos 3 caracteres")
    
    return role.name.upper(), role.description.upper()