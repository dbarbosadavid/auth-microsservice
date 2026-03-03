from fastapi import APIRouter, Depends, HTTPException

from model.roles import CreateRoleRequestBody
from services import roles_service, token_service


roles = APIRouter(prefix='/roles', tags=['Roles'])

@roles.get("/list", dependencies=[Depends(token_service.is_adm)])
def list_roles():
    return roles_service.get_all_roles()
    

@roles.post('/create', dependencies=[Depends(token_service.is_adm)])
def create_role(request: CreateRoleRequestBody):
    return roles_service.create_role(request)

@roles.put('/update/{id}', dependencies=[Depends(token_service.is_adm)])
def update_role(id: str, request: CreateRoleRequestBody):
    return roles_service.update_role(id, request)


@roles.delete('/delete/{id}', dependencies=[Depends(token_service.is_adm)])
def delete_role(id: str):
    return roles_service.delete_role(id)

@roles.get('/get/{id}', dependencies=[Depends(token_service.is_adm)])
def get_role_by_id(id: str):
    return roles_service.get_role_by_id(id)