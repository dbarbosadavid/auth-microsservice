from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

class UserCreateRequestBody (BaseModel):
    name: str = Field(examples=['JOSE MARIA'])
    email: str = Field(examples=['email@email.com'])
    password: str = Field(examples=['senha123'])

class UserAdminCreateRequestBody (UserCreateRequestBody):
    roles: str = Field(examples=['ADMIN,USER'])

class UserUpdateRequestBody (BaseModel):
    name: str = Field(examples=['JOSE MARIA'])
    password: str = Field(examples=['senha123'])

class UserAdminUpdateRequestBody (UserUpdateRequestBody):
    roles: str = Field(examples=['ADMIN,USER'])

class UserResponseBody (BaseModel):
    id: str = Field(examples=['id'])
    name: str = Field(examples=['JOSE MARIA'])
    email: str = Field(examples=['email@email.com'])
    hashed_password: str = Field(examples=['hashed_password'])
    roles: List[str] = Field(examples=[['ADMIN', 'USER']])
    created_at: datetime
    updated_at: datetime