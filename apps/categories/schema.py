from datetime import datetime

from pydantic import BaseModel

class CatProdOut(BaseModel):
    id_product: int
    name_product: str
    brand: int
    #categories_id: int
    price: int
    discount: int
    quantity_in_stock: int
    rating: float
    date_created: datetime
    date_update: datetime
    status: str
    img: str
    in_cart: bool

    class Config:
        orm_mode = True

class CatComOut(BaseModel):
    category: str
    count: int

    class Config:
        orm_mode = True