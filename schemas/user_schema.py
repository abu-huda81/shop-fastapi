from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone


class UserBase(BaseModel):
    username: str
    email: str
    roles: Optional[str] = "user"
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    message: str


class ErrorRsponse(BaseModel):
    message: str


class RoleBase(BaseModel):
    name: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    roles: Optional[List[str]] = None


class UserData(BaseModel):
    id: int