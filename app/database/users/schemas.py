from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8, max_length=255)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    is_active: Optional[bool]
    full_name: Optional[str] = Field(..., min_length=8, max_length=50)
    last_login: Optional[datetime]
    profile_image: Optional[str] = Field(..., min_length=8, max_length=255)
    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class UserDelete(BaseModel):
    detail: str
    model_config = {"from_attributes": True}
