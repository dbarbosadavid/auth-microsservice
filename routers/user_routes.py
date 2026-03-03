from services import token_service, user_service
from fastapi import APIRouter, Depends

from model.user import CreateUserRequestBody, UpdateUserRequestBody, UserResponseBody

user = APIRouter(prefix='/user', tags=['Users'])

@user.get('/list', response_model=list(), dependencies=[Depends(token_service.is_adm)])
def list_users():
    return user_service.get_all_users()

@user.post('/register', dependencies=[Depends(token_service.is_adm)])
def register_user(request: CreateUserRequestBody):
    return user_service.create_user(request)

@user.put('/update/{id}', dependencies=[Depends(token_service.is_adm)])
def update_user(id: str, request: UpdateUserRequestBody):
    return user_service.update_user(id, request)

@user.delete('/delete/{id}', dependencies=[Depends(token_service.is_adm)])
def delete_user(id: str):
    return user_service.delete_user(id)

@user.get('/get/{id}', response_model=UserResponseBody, dependencies=[Depends(token_service.is_adm)])
def get_user_by_id(id: str):
    return user_service.get_user_by_id(id)