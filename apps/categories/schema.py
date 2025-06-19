from datetime import datetime

from pydantic import BaseModel, Field

class CatProdOut(BaseModel):
    id_product: int
    name_product: str
    brand: str  # Изменено с int на str
    price: float
    discount: str  # Или int, если нужно хранить только процент
    quantity_in_stock: int
    rating: float
    date_created: datetime = Field(alias="date_create")  # Маппинг поля
    date_update: datetime
    status: str
    img: str
    in_cart: bool
    in_fav: bool

    class Config:
        orm_mode = True

class CatComOut(BaseModel):
    category: str
    url:str
    count: int

    class Config:
        orm_mode = True
