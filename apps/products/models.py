from fastapi import Query
from pydantic import BaseModel
from typing import List
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class NewProduct(BaseModel):
    name_product: str
    action_id: int
    categories_id: int
    brand: str
    price: int
    status: str
    img: str

class AddProdBask(BaseModel):
    #id_profile: int
    id_product: int
    #count: int| None = Query(default=1,  description="число товара")

class CheckoutItem(BaseModel):
    id_us_storage: int

# class CheckoutOrderRequest(BaseModel):
#     basket_items: List[CheckoutItem]
#     comment: str = ""
#     adress: str
#     shipping_cost: int
#     organization: str | None = None

from typing import Optional
class CheckoutOrderRequest(BaseModel):
    comment: Optional[str] = None
    shipping_cost: int = 0
    adress: Optional[str] = None


class Product(Base):
    __tablename__ = "Products"

    action_id: Mapped[int] = mapped_column(primary_key=True)  # id продукта
    name_product: Mapped[str] = mapped_column(String(255))
    categories_id: Mapped[int]
    brand: Mapped[str]
    price: Mapped[int]
    status: Mapped[str]
    img: Mapped[str]

