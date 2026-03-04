from model.schemas.token import TokenAuthResponseBody, TokenAuthRequestBody, TokenValidateResponseBody
from services.token_service import TokenService
from fastapi import APIRouter, Depends
from config.dependencies import get_current_user

token = APIRouter(prefix='/token', tags=['Token'])
token_service = TokenService()

@token.post('/auth', response_model=TokenAuthResponseBody)
def authenticate(form: TokenAuthRequestBody):
    return token_service.authenticate(form)

@token.post("/validate", dependencies=[Depends(get_current_user)], response_model=TokenValidateResponseBody)
def validate(current_user = Depends(get_current_user)):
    return TokenValidateResponseBody(
        id=current_user.id,
        email=current_user.email
    )

