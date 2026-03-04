from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import jwt, JWTError
from config import crypt
from config.env_variables import secret_key
from http import HTTPStatus

from model.schemas.token import TokenAuthResponseBody, TokenAuthRequestBody
from services.user_service import UserService

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class TokenService:
    def __init__(self):
        self.user_service = UserService()

    def create_access_token(self, data: dict):
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

    def validate_token(self, http_bearer):
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
        user = self.user_service.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user

    def authenticate(self, form: TokenAuthRequestBody):
        user = self.user_service.get_user_by_email(form.email)

        if not user or not crypt.verify_password(form.password, user.hashed_password):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas")

        token, expire_at = self.create_access_token(
            data={"sub": user.id}
        )
        return TokenAuthResponseBody (
            access_token=token,
            expire_at=expire_at,
            token_type="Bearer"
        )
