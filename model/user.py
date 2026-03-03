from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel

class CreateUserRequestBody (BaseModel):
    name: str
    email: str
    password: str
    roles: str

class UpdateUserRequestBody (BaseModel):
    name: str
    password: str
    roles: str

class UserResponseBody (BaseModel):
    id: str
    name: str
    email: str
    hashed_password: str
    roles: List[str]
    created_at: datetime
    updated_at: datetime

class User:
    name: str
    email: str
    hashed_password: str
    roles: List[str]
    created_at: datetime
    updated_at: datetime

    def __init__(self, name, email, hashed_password, roles, created_at, updated_at):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.roles = roles
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'hashed_password': self.hashed_password,
            'roles': self.roles,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }