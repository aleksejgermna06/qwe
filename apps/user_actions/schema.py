from datetime import datetime

from pydantic import BaseModel


class UserActionBase(BaseModel):
    product_id: int
    action_type: str


class UserActionCreate(UserActionBase):
    pass




class UserAction(UserActionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class UserActionOut(BaseModel):
    id_product: int
    name_product: str
    action_id: int
    categories_id: int
    brand: str
    price: int
    status: str
    img: str
    rating: float
    in_cart: bool

    class Config:
        orm_mode = True

