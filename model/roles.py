from datetime import datetime
from pydantic import BaseModel

class CreateRoleRequestBody (BaseModel):
    name: str
    description: str

class RoleResponseBody (BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

class Role:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, name, description, created_at, updated_at):
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }