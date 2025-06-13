from fastapi import Query
from pydantic import BaseModel
from typing import List

class NewCatProdCom(BaseModel):
    profile_id: int
    product_id: int