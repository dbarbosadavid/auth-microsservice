from typing import List

from fastapi import APIRouter, Depends

from config.dependencies import get_admin_user
from model.schemas.roles import RoleCreateRequestBody, RoleResponseBody
from services.roles_service import RolesService
from services.token_service import TokenService

token_service = TokenService()
roles_service = RolesService()

roles = APIRouter(prefix='/roles', tags=['Roles'])


@roles.get("/list",
           dependencies=[Depends(get_admin_user)],
           response_model=List[RoleResponseBody],
           responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def list_roles():
    return roles_service.get_all_roles()
    
@roles.post('/create', 
            status_code=201,
            response_description='Role criada com sucesso',
            dependencies=[Depends(get_admin_user)], 
            response_model=RoleResponseBody,
            responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def create_role(role_data: RoleCreateRequestBody):
    return roles_service.create_role(role_data)

@roles.put('/update/{id}',
           status_code=201,
           response_description='Role atualizada com sucesso',
           dependencies=[Depends(get_admin_user)], 
           response_model=RoleResponseBody,
           responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def update_role(id: str, role_data: RoleCreateRequestBody):
    return roles_service.update_role(id, role_data)

@roles.delete('/delete/{id}', 
              status_code=204, 
              response_description='Role deletada com sucesso',
              dependencies=[Depends(get_admin_user)],
              responses={
                  403: {"description": "Acesso negado: Requer permissão de administrador"}
               })
def delete_role(id: str):
    return roles_service.delete_role(id)

@roles.get('/get/{id}', 
           response_description='Role obtida com sucesso',
           dependencies=[Depends(get_admin_user)], 
           response_model=RoleResponseBody,
           responses={
               403: {"description": "Acesso negado: Requer permissão de administrador"}
            })
def get_role_by_id(id: str):
    return roles_service.get_role_by_id(id)