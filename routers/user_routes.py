from typing import List

from services.token_service import TokenService
from services.user_service import UserService
from fastapi import APIRouter, Depends

from config.dependencies import get_admin_user
from model.schemas.user import UserCreateRequestBody, UserUpdateRequestBody, UserResponseBody

user = APIRouter(prefix='/user', tags=['Users'])
user_service = UserService()
token_service = TokenService()

@user.get('/list', 
          response_model=List[UserResponseBody], 
          dependencies=[Depends(get_admin_user)],
          responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def list_users():
    return user_service.get_all_users()

@user.post('/register', 
           status_code=201,
           response_description='Usuário criado com sucesso',
           response_model=UserResponseBody,
           dependencies=[Depends(get_admin_user)],
           responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def register_user(request: UserCreateRequestBody):
    return user_service.create_user(request)
    
@user.put('/update/{id}',
          status_code=201,
          response_description='Usuário atualizado com sucesso',
          response_model=UserResponseBody,
          dependencies=[Depends(get_admin_user)],
          responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def update_user(id: str, request: UserUpdateRequestBody):
    return user_service.update_user(id, request)

@user.delete('/delete/{id}', 
             status_code=204, 
             response_description='Usuário deletado com sucesso',
             dependencies=[Depends(get_admin_user)],
             responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def delete_user(id: str):
    return user_service.delete_user(id)

@user.get('/get/{id}', 
          response_description='Usuário obtido com sucesso',
          response_model=UserResponseBody, 
          dependencies=[Depends(get_admin_user)],
          responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def get_user_by_id(id: str):
    return user_service.get_user_by_id(id)