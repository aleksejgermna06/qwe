from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AddPhone(BaseModel):
    telephone: Optional[str] = Field(max_length=15)

    @field_validator("telephone")
    def validate_telephone(cls, v: str) -> str:
        if not v.startswith("+"):
            raise ValueError("Телефон должен начинаться с '+'")
        if not v[1:].isdigit():
            raise ValueError("Телефон должен содержать только цифры от 0 до 9")
        return v

