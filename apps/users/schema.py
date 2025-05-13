from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class TokenResponse(BaseModel):
    __table_args__ = {'extend_existing': True}
    access_token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = "bearer"

class ProfileCreate(BaseModel):
    mail: EmailStr
    phone: Optional[str] = None
    name: Optional[str] = None
    password: str = Field(..., min_length=6)
    birthday: Optional[str] = None
    gender: Optional[str] = None

class LoginRequest(BaseModel):
    mail: EmailStr
    password: str

class ProfileResponse(BaseModel):
    id_profile: int
    mail: str
    name: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[str] = None
    bonus: int

    class Config:
        from_attributes = True