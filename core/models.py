import datetime
from sqlalchemy import String, MetaData, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base



class Profile(Base):
    __tablename__ ="Profile"
    id_profile: Mapped[int]=mapped_column(primary_key=True)
    date_created: Mapped[datetime.datetime] =mapped_column(server_default=text("TIMEZONE('utc', now())"))
    date_update: Mapped[datetime.datetime] =mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
    mail: Mapped[str]
    phone: Mapped[str | None] = mapped_column(nullable=True, default=None)
    name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    password: Mapped[str]
    birthday: Mapped[str | None] = mapped_column(nullable=True, default=None)#data
    gender: Mapped[str | None] = mapped_column(nullable=True, default=None)

    bonus: Mapped[int] = mapped_column(default=0)


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     #username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     hashed_password = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)
#
# class Token(Base):
#     __tablename__ = "user_tokens"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     access_token = Column(String, unique=True, nullable=False)
#     refresh_token = Column(String, unique=True, nullable=False)
#     expires_at = Column(DateTime, nullable=False)
#     is_active = Column(Boolean, default=True)

class Token(Base):
    __tablename__ = "user_tokens"
    __table_args__ = {'extend_existing': True}

    id_token: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(ForeignKey("Profile.id_profile", ondelete="CASCADE"))
    access_token: Mapped[str] = mapped_column(String(512), unique=True)
    refresh_token: Mapped[str] = mapped_column(String(512), unique=True)
    expires_at: Mapped[datetime.datetime]
    #is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

class Additional_telephone(Base):
    __tablename__ ="Additional_telephone"
    id_add_teleph: Mapped[int]=mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(ForeignKey("Profile.id_profile", ondelete="CASCADE"))
    telephone: Mapped[str]

class organization(Base):
    __tablename__ ="organization"
    id_organization:  Mapped[int]=mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(ForeignKey("Profile.id_profile", ondelete="CASCADE"))
    organization: Mapped[str]

class adress(Base):
    __tablename__ ="adress"
    id_adress:  Mapped[int]=mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(ForeignKey("Profile.id_profile", ondelete="CASCADE"))
    adress: Mapped[str]

class Categories(Base):
    __tablename__ = "Categories"
    id_categories: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(250))
    # product_id: Mapped[int] = mapped_column(ForeignKey("Product.id_product", ondelete="CASCADE"))
    name_categories: Mapped[str] = mapped_column(String(50))
    id_parent: Mapped[int | None] = mapped_column(nullable=True, default=None)


class Action(Base):
    __tablename__ = "Action"
    id_action: Mapped[int] = mapped_column(primary_key=True)
    # id_product: Mapped[int] = mapped_column(ForeignKey("Product.id_product", ondelete="CASCADE"))
    action: Mapped[str] = mapped_column(String(50))
    discount: Mapped[int]

class Product(Base):
    __tablename__ = "Product"
    id_product: Mapped[int] = mapped_column(primary_key=True)
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
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id_product", ondelete="CASCADE"), primary_key=True
    )
    id_gfields: Mapped[int] = mapped_column(
        ForeignKey("Gfields.id_gfields", ondelete="CASCADE"), primary_key=True
    )
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
    count: Mapped[int]

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

class UserAction(Base):
    __tablename__ = "UserAction"
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
    action: Mapped[str] = mapped_column(String(50))

class Order(Base):
    __tablename__ = "Order"
    id_order: Mapped[int] = mapped_column(primary_key=True)
    id_product: Mapped[int] = mapped_column(
        ForeignKey("Product.id_product", ondelete="CASCADE")
    )
    id_profile: Mapped[int] = mapped_column(
        ForeignKey("Profile.id_profile", ondelete="CASCADE")
    )
    count: Mapped[int]

class OrderProcessor(Base):
    __tablename__ = "Order_processor"
    id_order_proc: Mapped[int] = mapped_column(primary_key=True)
    id_order: Mapped[int] = mapped_column(ForeignKey("Order.id_order"))
    date_created: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    date_update: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
    price: Mapped[int]
    date_delivery: Mapped[int]
    count: Mapped[int]
    status: Mapped[str] = mapped_column(String(50))
    comment: Mapped[str] = mapped_column(String(350))
    shipping_cost: Mapped[int]
    adress: Mapped[str] = mapped_column(String(50))
    organization: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None
    )







metadata_obj=MetaData()

