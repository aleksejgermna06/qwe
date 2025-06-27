from pydantic import BaseModel
from typing import List, Optional

class ProductInOrder(BaseModel):
    name_product: str
    price: int
    count: int

class UserOrderResponse(BaseModel):
    id_order_proc: int
    total_price: int
    count: int
    status: str
    comment: Optional[str]
    shipping_cost: int
    adress: Optional[str]
    products: List[ProductInOrder]

    class Config:
        from_attributes = True

