import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, text, ForeignKey
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
#Указывать размеры
    phone: Mapped[str | None] = mapped_column(nullable=True, default=None)
    name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    password: Mapped[str]
    birthday: Mapped[str | None] = mapped_column(nullable=True, default=None)#data
    gender: Mapped[str | None] = mapped_column(nullable=True, default=None)

    bonus: Mapped[int] = mapped_column(default=0)


class Token(Base):
    __tablename__ = "user_tokens"
    __table_args__ = {'extend_existing': True}

    id_token: Mapped[int] = mapped_column(primary_key=True)
    id_profile: Mapped[int] = mapped_column(ForeignKey("Profile.id_profile", ondelete="CASCADE"))
    access_token: Mapped[str] = mapped_column(String(512), unique=True)
    refresh_token: Mapped[str] = mapped_column(String(512), unique=True)
    expires_at: Mapped[datetime.datetime]
    is_active: Mapped[bool] = mapped_column(default=True)
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



metadata_obj=MetaData()

