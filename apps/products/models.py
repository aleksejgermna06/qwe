from pydantic import BaseModel


class NewProduct(BaseModel):
    name_product: str
    action_id: int
    categories_id: int
    brand: str
    price: int
    status: str
    img: str
