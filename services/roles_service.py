from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException

from model.schemas.roles import RoleCreateRequestBody, RoleResponseBody
from model.dto.role_dto import RoleDTO
from repository.role_repsitory import RoleRepository

class RolesService:
    def __init__(self):
        self.repo = RoleRepository()

    def get_all_roles(self):
        roles = self.repo.get_all()

        if not roles:
            return []
        
        return [
            RoleResponseBody(
                id=id,
                name=role['name'],
                description=role['description'],
                created_at=role['created_at'],
                updated_at=role['updated_at']
            )
            for id, role in roles.items()
        ]



    def create_role(self, new_role: RoleCreateRequestBody):
        name, description = self.validate_role_data(new_role)
        timestamp = datetime.now()
        new_role = RoleDTO(
            name=name,
            description=description,
            created_at=timestamp,
            updated_at=timestamp
        )
        
        id = self.repo.create(new_role.to_json())

        return RoleResponseBody(
            id=id.key,
            name=new_role.name,
            description=new_role.description,
            created_at=new_role.created_at,
            updated_at=new_role.updated_at
        )



    def update_role(self, id, new_role: RoleCreateRequestBody):
        role_exist = self.get_role_by_id(id)
        name, description = self.validate_role_data(new_role)
        
        role = RoleDTO(
            name=name,
            description=description,
            created_at=role_exist.created_at,
            updated_at=datetime.now())

        self.repo.update(id, role.to_json())

        return RoleResponseBody(
            id=id,
            name=role.name,
            description=role.description,
            created_at=role.created_at,
            updated_at=role.updated_at
        )



    def delete_role(self, id):
        role = self.get_role_by_id(id)
        self.repo.delete(id)
        return {
            "message": "Role deletada com sucesso"
        }



    def get_role_by_id(self, id):
        role_found = self.repo.get_by_id(id)

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



    def validate_role_data(role: RoleCreateRequestBody):
        if len(role.name) < 3:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="O nome da role deve conter pelo menos 3 caracteres")
        
        if len(role.description) < 3:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="A descrição da role deve conter pelo menos 3 caracteres")
        
        return role.name.upper(), role.description.upper()