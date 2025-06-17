from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_async_db
from core.security import get_current_user
from core.models import Profile
from apps.user_actions.service import get_user_actions, add_user_action, delete_favorite
from apps.user_actions.schema import UserActionOut
from typing import List, Literal

from apps.user_actions import service

router = APIRouter(prefix="/user/actions", tags=["user actions"])


@router.get("/{action_type}", response_model=List[UserActionOut])
async def get_actions(
    action_type: Literal["favorite", "view"],
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    return await get_user_actions(current_user.id_profile, action_type, db)


@router.post("/{action_type}/{product_id}", response_model=dict)
async def add_action(
    action_type: Literal["favorite", "view"],
    product_id: int,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    await add_user_action(current_user.id_profile, product_id, action_type, db)
    return {"message": f"{action_type} added for product {product_id}"}


@router.delete("/favorite/{product_id}", response_model=dict)
async def remove_favorite(
    product_id: int,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    await delete_favorite(current_user.id_profile, product_id, db)
    return {"message": f"Favorite for product {product_id} removed"}
