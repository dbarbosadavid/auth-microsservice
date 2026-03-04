from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from services.token_service import TokenService

oauth2_scheme = HTTPBearer()

def get_current_user(credentials: str = Depends(oauth2_scheme)):
    auth_service = TokenService()
    return auth_service.validate_token(credentials)

def get_admin_user(user=Depends(get_current_user)):
    if "ADM" not in user.roles:
        raise HTTPException(status_code=403, detail="Acesso negado: Requer permissão de administrador")
    return user