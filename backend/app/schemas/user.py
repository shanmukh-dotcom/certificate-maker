from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    organization_id: int

class UserOut(UserBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

