from typing import List

from sqlalchemy.orm import Session

from core.models import UserAction
from core.database import get_async_db
from sqlalchemy import select
from apps.products.service import ProductService
from core.models import UserAction



session_fabrik = get_async_db
class UserActionService:
    def __init__(self, db: Session):
        self.db = db



    async def get_user_view_history(self, user_id: int) -> list[dict]:
        async for session in session_fabrik():
            result = await session.execute(
                select(UserAction.product_id)
                .where(UserAction.profile_id == user_id, UserAction.action == "view")
                .order_by(UserAction.date_created.desc())
            )
            product_ids = [row[0] for row in result.fetchall()]
            if not product_ids:
                return []

            # Получаем данные о продуктах пачкой
            products = await ProductService.get_many_products(product_ids)
            return products

    def create_action(
        self, user_id: int, product_id: int, action_type: str
    ) -> UserAction:
        action = UserAction(
            user_id=user_id, product_id=product_id, action_type=action_type
        )
        self.db.add(action)
        self.db.commit()
        self.db.refresh(action)
        return action

    def delete_favorite(self, user_id: int, product_id: int) -> None:
        action = (
            self.db.query(UserAction)
            .filter(
                UserAction.profile_id == user_id,
                UserAction.product_id == product_id,
                UserAction.action == "favorite",
            )
            .first()
        )
        if action:
            self.db.delete(action)
            self.db.commit()


    def get_user_favorites(self, user_id: int) -> List[UserAction]:
        return (
            self.db.query(UserAction)
            .filter(UserAction.profile_id == user_id, UserAction.action == "favorite")
            .all()
        )

    # def get_user_view_history(self, user_id: int) -> List[UserAction]:
    #     return (
    #         self.db.query(UserAction)
    #         .filter(UserAction.user_id == user_id, UserAction.action_type == "view")
    #         .order_by(UserAction.created_at.desc())
    #         .all()
    #     )




