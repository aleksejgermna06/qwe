from pydantic import BaseModel
from datetime import datetime


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