from datetime import datetime

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base

# class UserAction(Base):
#     __tablename__ = "UserAction"
#     __table_args__ = {'extend_existing': True}
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
#     action_type: Mapped[str] = mapped_column(String(50))  # 'view' или 'favorite'
#     created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
#     updated_at: Mapped[datetime] = mapped_column(
#         server_default=text("TIMEZONE('utc', now())"),
#         onupdate=datetime.utcnow,
#     )
