from datetime import datetime
from pydantic import BaseModel, Field

class RoleCreateRequestBody (BaseModel):
    name: str = Field(examples=['USER'])
    description: str = Field(examples=['COMMON USER'])

class RoleResponseBody (BaseModel):
    id: str = Field(examples=['id'])
    name: str = Field(examples=['USER'])
    description: str = Field(examples=['COMMON USER'])
    created_at: datetime
    updated_at: datetime