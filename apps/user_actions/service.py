from typing import List

from sqlalchemy.orm import Session

from core.models import UserAction


class UserActionService:
    def __init__(self, db: Session):
        self.db = db

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
                UserAction.user_id == user_id,
                UserAction.product_id == product_id,
                UserAction.action_type == "favorite",
            )
            .first()
        )
        if action:
            self.db.delete(action)
            self.db.commit()

    def get_user_favorites(self, user_id: int) -> List[UserAction]:
        return (
            self.db.query(UserAction)
            .filter(UserAction.user_id == user_id, UserAction.action_type == "favorite")
            .all()
        )

    def get_user_view_history(self, user_id: int) -> List[UserAction]:
        return (
            self.db.query(UserAction)
            .filter(UserAction.user_id == user_id, UserAction.action_type == "view")
            .order_by(UserAction.created_at.desc())
            .all()
        )
