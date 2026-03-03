from datetime import datetime
from pydantic import BaseModel

class LoginRequestBody (BaseModel):
    email: str
    password: str

class AuthenticateResponseBody (BaseModel):
    access_token: str
    expire_in: datetime
    token_type: str