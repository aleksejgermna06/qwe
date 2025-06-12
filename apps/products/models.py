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
