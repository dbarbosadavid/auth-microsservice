from config.crypt import verify_password
from model.token import AuthenticateResponseBody, LoginRequestBody
from services import token_service
from fastapi import APIRouter, Depends, HTTPException


token = APIRouter(prefix='/token', tags=['Token'])

@token.post('/auth', response_model=AuthenticateResponseBody)
def authenticate(form: LoginRequestBody):
    return token_service.authenticate(form)


@token.get("/validate")
def validate(current_user = Depends(token_service.validate_token)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

