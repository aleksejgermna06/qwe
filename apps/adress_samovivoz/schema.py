from pydantic import BaseModel

class AdressIn(BaseModel):
    adress: str

class AdressOut(BaseModel):
    id: int
    adress: str