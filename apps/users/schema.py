from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProfileCreate(BaseModel):
    mail: EmailStr
    phone: Optional[str] = None
    #phone: str = Field(..., min_length=5)
    name: Optional[str] = None
    #name: str
    password: str = Field(..., min_length=6)
    #birthday: str
    birthday: Optional[str] = None
    #gender: str
    gender: Optional[str] = None

class LoginRequest(BaseModel):
    mail: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ProfileResponse(BaseModel):
    id_profile: int
    mail: str
    name: str
    phone: str
    birthday: str
    gender: str
    bonus: int

    class Config:
        from_attributes = True