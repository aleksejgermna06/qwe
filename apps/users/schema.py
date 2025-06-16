
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime, date

class TokenResponse(BaseModel):
    __table_args__ = {'extend_existing': True}
    access_token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = "bearer"

class AdressResponse(BaseModel):
    id: int = Field(alias="id_adress")
    settlement: str
    street: str
    entrance: str
    flor: str
    aptOffice: str = Field(alias="apt_office")
    isMain: bool = Field(alias="is_main")

    class Config:
        from_attributes = True
        populate_by_name = True

class ProfileCreate(BaseModel):
    mail: EmailStr
    phone: Optional[str] = None
    name: Optional[str] = None
    password: str = Field(..., min_length=6)
    birthday: Optional[str] = None
    gender: Optional[str] = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=15)
    birthday: Optional[date] = None
    gender: Optional[str] = Field(default=None, max_length=10)

    @field_validator("gender")
    def validate_gender(cls, v):
        allowed = {"Мужской", "Женский",None}
        if v and v.lower() not in allowed:
            raise ValueError("Гендер должен быть 'Мужской' или 'Женский'")
        return v

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
    #addresses: Optional[List[AdressResponse]] = None

    class Config:
        from_attributes = True
        orm_mode = True

class LoginProfileResponse(BaseModel):
    id_profile: int
    mail: str
    name: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[str] = None
    bonus: int

    class Config:
        orm_mode = True

class AdressCreate(BaseModel):
    settlement: str
    street: str
    entrance: str
    flor: str
    aptOffice: str
    isMain: bool = False

class AdressUpdate(BaseModel):
    settlement: Optional[str]
    street: Optional[str]
    entrance: Optional[str]
    flor: Optional[str]
    aptOffice: Optional[str]
    isMain: Optional[bool]
