from fastapi import Query
from pydantic import BaseModel
from typing import List

class NewProduct(BaseModel):
    name_product: str
    action_id: int
    categories_id: int
    brand: str
    price: int
    status: str
    img: str

class AddProdBask(BaseModel):
    id_profile: int
    id_product: int
    count: int| None = Query(default=1,  description="число товара")

class CheckoutItem(BaseModel):
    id_us_storage: int

class CheckoutOrderRequest(BaseModel):
    basket_items: List[CheckoutItem]
    comment: str = ""
    adress: str
    shipping_cost: int
    organization: str | None = None
