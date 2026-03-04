from datetime import datetime

from fastapi import HTTPException
from http import HTTPStatus
from config.crypt import hash_password
from model.schemas.user import UserUpdateRequestBody, UserCreateRequestBody, UserResponseBody
from model.dto.user_dto import UserDTO
from email_validator import validate_email, EmailNotValidError

from repository.user_repository import UserRepository
from services.roles_service import RolesService

class UserService:
    def __init__(self):
        self.repo = UserRepository()
        self.roles_service = RolesService()

    def create_user(self, user: UserCreateRequestBody):
        name, email, hashed_password, roles = self.validate_user_data(user)

        timestamp = datetime.now()
        new_user = UserDTO(
            name=name,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
            created_at=timestamp,
            updated_at=timestamp)

        new_db_user = self.repo.create(new_user.to_json())
        roles = self.roles_service.get_all_roles()

        return UserResponseBody(
            id=new_db_user.key,
            name=new_user.name,
            email=new_user.email,
            hashed_password=hashed_password,
            roles=[
                role.name for role in roles if role.id in new_user.roles
            ],
            created_at=new_user.created_at,
            updated_at=new_user.updated_at)


    def update_user(self, id: str, user_request: UserUpdateRequestBody):
        user_exist = self.get_user_by_id(id)

        name, email, hashed_password, roles = self.validate_user_data(user_request)
        email = user_exist.email
        
        new_user = UserDTO(
            name=name,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
            updated_at=datetime.now(),
            created_at=user_exist.created_at)

        roles = self.roles_service.get_all_roles()
        self.repo.update(id, new_user.to_json())
        return UserResponseBody(
            id=id,
            name=new_user.name,
            email=new_user.email,
            hashed_password=hashed_password,
            roles=[
                role.name for role in roles if role.id in new_user.roles
            ],
            created_at=user_exist.created_at,
            updated_at=new_user.updated_at)

    def delete_user(self, id: str):
        user_exist = self.get_user_by_id(id)
        self.repo.delete(id)
        return {
            "message": "Usuário deletado com sucesso",
        }


    def get_user_by_email(self, email_search: str):
        users = self.repo.get_all()
        
        if users:
            for id, user in users.items():
                if user['email'] == email_search:
                    user_found = UserResponseBody (
                        id=id,
                        name=user['name'],
                        email=user['email'],
                        hashed_password=user['hashed_password'],
                        roles=user['roles'] if 'roles' in user else [],
                        created_at=user['created_at'],
                        updated_at=user['updated_at'])
                    return user_found
        
        return None



    def get_user_by_id(self, id: str):
        user_found = self.repo.get_by_id(id)
        roles = self.roles_service.get_all_roles()

        if user_found:
            user = UserResponseBody (
                id=id,
                name=user_found['name'],
                email=user_found['email'],
                hashed_password=user_found['hashed_password'],
                roles=[
                    role.name for role in roles if role.id in user_found['roles']
                ],
                created_at=user_found['created_at'],
                updated_at=user_found['updated_at'])
            return user
        
        raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="ID não encontrado")



    def validate_user_data(self, user: UserCreateRequestBody | UserUpdateRequestBody):
        if len(user.name) < 3:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="O nome de usuário deve ter pelo menos 3 caracteres")
        
        if len(user.password) < 8:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="A senha deve ter pelo menos 8 caracteres")
        
        roles = user.roles.upper()
        roles = roles.split(',')

        valid_roles = self.roles_service.get_all_roles()
        valid_roles_names = [role['name'] for role in valid_roles]
        valid_roles_id = []

        for role in roles:
            if role not in valid_roles_names:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Role '{role}' é inválida. As roles válidas são: {', '.join(valid_roles_names)}")
            else:
                idx = valid_roles_names.index(role) 
                valid_roles_id.append(valid_roles[idx]['id'])

        if hasattr(user, 'email'):
            new_email = self.validate_new_email(user.email)
        else: 
            new_email = None

        name = user.name.upper()
        password = hash_password(user.password)
        
        return name, new_email, password, valid_roles_id



    def validate_new_email(self, new_email: str):
        try:
            new_email = validate_email(new_email).normalized
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Email inválido: {e.args}")
        
        email_in_use = self.get_user_by_email(new_email)

        if email_in_use:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email não disponível")
        else:
            return new_email


    def get_all_users(self):
        users = self.repo.get_all()
        roles = self.roles_service.get_all_roles()

        if not users:
            return []
        
        return [
            UserResponseBody (
                id = id,
                name = user['name'],
                email = user['email'],
                hashed_password = user['hashed_password'],
                roles = [
                    role.name for role in roles if role.id in user['roles']
                ],
                created_at = user['created_at'],
                updated_at = user['updated_at'])
            for id, user in users.items()
        ]