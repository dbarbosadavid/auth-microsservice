from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jose import jwt, JWTError
from config import crypt
from config.env_variables import secret_key
from http import HTTPStatus

from model.token import AuthenticateResponseBody, LoginRequestBody
from services import roles_service, user_service

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = HTTPBearer()


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now()
    })

    encoded_jwt = jwt.encode(
        to_encode,
        secret_key,
        algorithm=ALGORITHM,
    )

    return encoded_jwt, expire

def validate_token(http_bearer: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            http_bearer.credentials,
            secret_key,
            algorithms=[ALGORITHM]
        )

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # buscar usuário no Firebase
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user

def authenticate(form: LoginRequestBody):
    user = user_service.get_user_by_email(form.email)

    if not user or not crypt.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas")

    token, expire_in = create_access_token(
        data={"sub": user.id}
    )

    return AuthenticateResponseBody (
        access_token=token,
        expire_in=expire_in,
        token_type="Bearer"
    )

def is_adm(user = Depends(validate_token)):
    roles = roles_service.get_all_roles()

    for role_id in user.roles:
        for role in roles:
            if role['id'] == role_id and role['name'] == 'ADM':
                return True
        
    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail="Acesso negado: Requer permissão de administrador"
    )
