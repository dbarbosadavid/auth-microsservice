from datetime import datetime

from database.firebase import ref_users
from fastapi import HTTPException
from http import HTTPStatus
from config.crypt import hash_password
from model.user import UpdateUserRequestBody, User, CreateUserRequestBody, UserResponseBody
from email_validator import validate_email, EmailNotValidError

from services import roles_service


def create_user(user: CreateUserRequestBody):
    name, email, hashed_password, roles = validate_user_data(user)

    timestamp = datetime.now()
    new_user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        roles=roles,
        created_at=timestamp,
        updated_at=timestamp)

    new_db_user = ref_users.push(new_user.to_json())

    return UserResponseBody(
        id=new_db_user.key,
        name=new_user.name,
        email=new_user.email,
        hashed_password=hashed_password,
        roles=new_user.roles,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at)


def update_user(id: str, user_request: UpdateUserRequestBody):
    user_exist = get_user_by_id(id)

    name, email, hashed_password, roles = validate_user_data(user_request)
    email = user_exist.email
    
    new_user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        roles=roles,
        updated_at=datetime.now(),
        created_at=user_exist.created_at)

    ref_users.child(id).update(new_user.to_json())
    return UserResponseBody(
        id=id,
        name=new_user.name,
        email=new_user.email,
        hashed_password=hashed_password,
        roles=new_user.roles,
        created_at=user_exist.created_at,
        updated_at=new_user.updated_at)

def delete_user(id: str):
    user_exist = get_user_by_id(id)
    ref_users.child(id).delete()
    return {
        "message": "Usuário deletado com sucesso",
    }


def get_user_by_email(email_search: str):
    users = ref_users.get()
    
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



def get_user_by_id(id: str):
    user_found = ref_users.child(id).get()

    if user_found:
        user = UserResponseBody (
            id=id,
            name=user_found['name'],
            email=user_found['email'],
            hashed_password=user_found['hashed_password'],
            roles=user_found['roles'] if 'roles' in user_found else [],
            created_at=user_found['created_at'],
            updated_at=user_found['updated_at'])
        return user
    
    raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ID não encontrado")



def validate_user_data(user: CreateUserRequestBody | UpdateUserRequestBody):
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

    valid_roles = roles_service.get_all_roles()
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
        new_email = validate_new_email(user.email)
    else: 
        new_email = None

    name = user.name.upper()
    password = hash_password(user.password)
    
    return name, new_email, password, valid_roles_id



def validate_new_email(new_email: str):
    try:
        new_email = validate_email(new_email).normalized
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Email inválido: {e.args}")
    
    email_in_use = get_user_by_email(new_email)

    if email_in_use:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email não disponível")
    else:
        return new_email


def get_all_users():
    users = ref_users.get()
    users_list = list()

    if users:
        for id, user in users.items():
            print(user)
            current_user = UserResponseBody (
                id = id,
                name = user['name'],
                email = user['email'],
                hashed_password = user['hashed_password'],
                roles = user['roles'] if 'roles' in user else [],
                created_at = user['created_at'],
                updated_at = user['updated_at'])
            users_list.append(current_user)
        return users_list
    
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Sem usuários cadastrados")