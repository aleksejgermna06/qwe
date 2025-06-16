from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, text
import datetime
from core.database import Base

class UserAction(Base):
    __tablename__ = "UserActions"
    __table_args__ = {'extend_existing': True}

    id_action: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("Product.id_product", ondelete="CASCADE")
    )
    date_created: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    date_update: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
    action: Mapped[str] = mapped_column(String(50))  # 'favorite' или 'view'
