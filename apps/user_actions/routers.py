from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_async_db
from .service import UserActionService
from core.models import UserAction
from .schema import UserAction, UserActionCreate
from core.security import get_current_user

from .schema import UserAction, UserActionCreate

from .service import UserActionService

router = APIRouter(prefix="/user_actions", tags=["user_actions"])
#UserAction
@router.post("/favorites", response_model=UserAction, summary="Добавить в избранное")
def add_to_favorites(
    product_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    service = UserActionService(db)
    return service.create_action(current_user.id_profile, product_id, "favorite")


@router.delete("/favorites/{product_id}", summary="убрать из избранного")
def remove_from_favorites(
    product_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    service = UserActionService(db)
    service.delete_favorite(current_user.id_profile, product_id)
    return {"message": "Removed from favorites"}


@router.get(
    "/favorites", response_model=list[UserAction], summary="посмотреть избранные"
)
def get_favorites(
    current_user = Depends(get_current_user), db: Session = Depends(get_async_db)
):
    service = UserActionService(db)
    return service.get_user_favorites(current_user.id_profile)


@router.get(
    "/view-history", response_model=list[UserAction], summary="просмотр истории"
)
def get_view_history(
    current_user = Depends(get_current_user), db: Session = Depends(get_async_db)
):
    service = UserActionService(db)
    return service.get_user_view_history(current_user.id_profile)


@router.post("/view", response_model=UserAction)
def add_to_view_history(
    product_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_async_db),
):
    service = UserActionService(db)
    return service.create_action(current_user.id_profile, product_id, "view")
