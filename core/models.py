import datetime
from datetime import datetime as dt
from sqlalchemy import Column, ForeignKey, Integer, String, text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Token(Base):
    __tablename__ = "user_tokens"
    __table_args__ = {"extend_existing": True}

    id_token: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    access_token: Mapped[str] = mapped_column(String(512), unique=True)
    refresh_token: Mapped[str] = mapped_column(String(512), unique=True)
    expires_at: Mapped[datetime.datetime]
    # is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )


class Profile(Base):
    __tablename__ = "Profile"
    id_profile: Mapped[int] = mapped_column(primary_key=True)
    date_created: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    date_update: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
    mail: Mapped[str]  # ????? = mapped_column()
    # phone: Mapped[str] = mapped_column(default="")
    # name: Mapped[str] = mapped_column(default="")
    # password: Mapped[str]
    # birthday: Mapped[str] = mapped_column(default="")
    # gender: Mapped[str] = mapped_column(default="")
    # bonus: Mapped[int] = mapped_column(default=0) ограничить размеры. relaphion ship. /puch. put/ qure/ token/ voleum conteiner postgress/декаратор

    phone: Mapped[str | None] = mapped_column(String(13), nullable=True, default=None)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    password: Mapped[str] = mapped_column(
        String(255)
    )  # оставлено обязательным, можно добавить default=None при необходимости
    birthday: Mapped[str | None] = mapped_column(
        String(10), nullable=True, default=None
    )  # 2025.02.25
    gender: Mapped[str | None] = mapped_column(nullable=True, default=None)
    bonus: Mapped[int] = mapped_column(default=0)

    #addresses = relationship("Adress", back_populates="profile", lazy="selectin")




class AdditionalTelephone(Base):
    __tablename__ = "Additional_telephone"
    id_add_teleph: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    telephone: Mapped[str] = mapped_column(String(13))


class Organization(Base):
    __tablename__ = "Organization"
    id_organization: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    organization: Mapped[str] = mapped_column(String(50))


# class adress(Base):
#     __tablename__ = "Adress"
#     id_adress: Mapped[int] = mapped_column(primary_key=True)
#     id_profile: Mapped[int] = mapped_column(
#         ForeignKey("Profile.id_profile", ondelete="CASCADE")
#     )
#     adress: Mapped[str] = mapped_column(String(50))


class adress(Base):
    __tablename__ = "Adress"

    id_adress = Column(Integer, primary_key=True, index=True)
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    settlement = Column(String)
    street = Column(String)
    entrance = Column(String)
    flor = Column(String)
    apt_office = Column(String)
    is_main = Column(Boolean, default=False)
    #profile = relationship("Profile", back_populates="addresses")



class Categories(Base):
    __tablename__ = "Categories"
    id_categories: Mapped[int] = mapped_column(primary_key=True)
    # product_id: Mapped[int] = mapped_column(ForeignKey("Product.id_product", ondelete="CASCADE"))
    name_categories: Mapped[str] = mapped_column(String(50))
    url: Mapped[str]
    id_parent: Mapped[int | None] = mapped_column(nullable=True, default=None)


class Action(Base):
    __tablename__ = "Action"
    id_action: Mapped[int] = mapped_column(primary_key=True)
    # id_product: Mapped[int] = mapped_column(ForeignKey("Product.id_product", ondelete="CASCADE"))
    action: Mapped[str] = mapped_column(String(50))
    discount: Mapped[int]


class Product(Base):
    __tablename__ = "Product"
    id_product: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("Action.id_action"))
    categories_id: Mapped[int] = mapped_column(ForeignKey("Categories.id_categories"))
    date_created: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    date_update: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
    name_product: Mapped[str]
    brand: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    price: Mapped[int] = mapped_column(default=0)
    # discount: Mapped[int]
    # number_of_reviews: Mapped[int]
    quantity_in_stock: Mapped[int] = mapped_column(default=0)
    rating: Mapped[int] = mapped_column(default=0)
    status: Mapped[str | None] = mapped_column(String(25), nullable=True, default=None)
    img: Mapped[str | None] = mapped_column(nullable=True, default=None)


class Gfields(Base):
    __tablename__ = "Gfields"
    id_gfields: Mapped[int] = mapped_column(primary_key=True)
    name_gfields: Mapped[str] = mapped_column(String(50))


class Entity(Base):
    __tablename__ = "Entity"
    product_id: Mapped[int] = mapped_column(
        ForeignKey("Product.id_product", ondelete="CASCADE"), primary_key=True
    )
    gfields_id: Mapped[int] = mapped_column(
        ForeignKey("Gfields.id_gfields", ondelete="CASCADE"), primary_key=True
    )
    name_har: Mapped[str] = mapped_column(String(350))
    cost_har: Mapped[str] = mapped_column(String(350))


class UserBasket(Base):
    __tablename__ = "User_basket"
    id_us_storage: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id_product", ondelete="CASCADE")
    )
    count: Mapped[int| None] = mapped_column(nullable=True, default=1)


class Reviews(Base):
    __tablename__ = "Reviews"
    id_reviews: Mapped[int] = mapped_column(primary_key=True)
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
    reviews: Mapped[str] = mapped_column(String(150))
    like: Mapped[int] = mapped_column(default=0)
    dislike: Mapped[int] = mapped_column(default=0)



#
# from typing import Optional
# from sqlalchemy import ForeignKey, String, text
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from datetime import datetime
# from typing import Optional
# from core.database import Base
#
# class OrderProcessor(Base):
#     __tablename__ = "Order_processor"
#
#     id_order_proc: Mapped[int] = mapped_column(primary_key=True)
#     id_order: Mapped[int] = mapped_column(ForeignKey("Order.id_order", ondelete="CASCADE"))
#
#     date_created: Mapped[datetime] = mapped_column(
#         server_default=text("TIMEZONE('utc', now())")
#     )
#     date_update: Mapped[datetime] = mapped_column(
#         server_default=text("TIMEZONE('utc', now())"),
#         onupdate=datetime.utcnow
#     )
#
#     price: Mapped[int]
#     date_delivery: Mapped[Optional[datetime]] = mapped_column(nullable=True)
#     count: Mapped[int]
#     status: Mapped[str] = mapped_column(String(50))
#     comment: Mapped[Optional[str]] = mapped_column(String(350), nullable=True)
#     shipping_cost: Mapped[int]
#     adress: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
#
#     # Связь с заказом
#     order: Mapped["Order"] = relationship("Order", backref="processor")


# class OrderProcessor(Base):
#     __tablename__ = "Order_processor"
#     id_order_proc: Mapped[int] = mapped_column(primary_key=True)
#     id_order: Mapped[int] = mapped_column(ForeignKey("Order.id_order"))
#     date_created: Mapped[datetime.datetime] = mapped_column(
#         server_default=text("TIMEZONE('utc', now())")
#     )
#     date_update: Mapped[datetime.datetime] = mapped_column(
#         server_default=text("TIMEZONE('utc', now())"),
#         onupdate=datetime.datetime.utcnow,
#     )
#     price: Mapped[int]
#     date_delivery: Mapped[Optional[dt]] = mapped_column(nullable=True)
#     count: Mapped[int]
#     status: Mapped[str] = mapped_column(String(50))
#     comment: Mapped[Optional[str]] = mapped_column(String(350), nullable=True)
#     shipping_cost: Mapped[int]
#     adress: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
#     organization: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base  # используем общий Base, а не локальный declarative_base()


class OrderGroup(Base):
    __tablename__ = "Order_group"

    id_order_group: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE"),
        nullable=False
    )
    date_created: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    date_update: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )

    # ORM-каскад: при удалении группы удалятся заказы и процессор
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="order_group",
        cascade="all, delete-orphan"
    )
    processor: Mapped[Optional["OrderProcessor"]] = relationship(
        "OrderProcessor",
        back_populates="order_group",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "Order"

    id_order: Mapped[int] = mapped_column(primary_key=True)
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id_product", ondelete="CASCADE"),
        nullable=False
    )
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE"),
        nullable=False
    )
    id_order_group: Mapped[int] = mapped_column(
        ForeignKey("Order_group.id_order_group", ondelete="CASCADE"),
        nullable=False
    )
    count: Mapped[int]

    order_group: Mapped["OrderGroup"] = relationship("OrderGroup", back_populates="orders")


class OrderProcessor(Base):
    __tablename__ = "Order_processor"

    id_order_proc: Mapped[int] = mapped_column(primary_key=True)
    id_order_group: Mapped[int] = mapped_column(
        ForeignKey("Order_group.id_order_group", ondelete="CASCADE"),
        nullable=False
    )
    date_created: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    date_update: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )

    price: Mapped[int]
    date_delivery: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    count: Mapped[int]
    status: Mapped[str] = mapped_column(String(50))
    comment: Mapped[Optional[str]] = mapped_column(String(350), nullable=True)
    shipping_cost: Mapped[int]
    adress: Mapped[str] = mapped_column(String(50))

    order_group: Mapped["OrderGroup"] = relationship("OrderGroup", back_populates="processor")



class ComparisonStore(Base):
    __tablename__ = "ComparisonStore"
    id_com_stor: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("Profile.id_profile", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("Product.id_product", ondelete="CASCADE"))


class AdressSamovivoz(Base):
    __tablename__ = "adress_samovivoz"

    id = Column(Integer, primary_key=True, index=True)
    adress = Column(String, unique=True, index=True)

