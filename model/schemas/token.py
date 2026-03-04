from datetime import datetime
from pydantic import BaseModel

class TokenAuthRequestBody (BaseModel):
    email: str
    password: str

class TokenAuthResponseBody (BaseModel):
    access_token: str
    expire_at: datetime
    token_type: str

class TokenValidateResponseBody (BaseModel):
    id: str
    email: str