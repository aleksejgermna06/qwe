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
    mail: Mapped[str]#????? = mapped_column()
    #phone: Mapped[str] = mapped_column(default="")
    #name: Mapped[str] = mapped_column(default="")
    #password: Mapped[str]
    #birthday: Mapped[str] = mapped_column(default="")
    #gender: Mapped[str] = mapped_column(default="")
    #bonus: Mapped[int] = mapped_column(default=0)


    phone: Mapped[str | None] = mapped_column(nullable=True, default=None)
    name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    password: Mapped[str]  # оставлено обязательным, можно добавить default=None при необходимости
    birthday: Mapped[str | None] = mapped_column(nullable=True, default=None)
    gender: Mapped[str | None] = mapped_column(nullable=True, default=None)
    bonus: Mapped[int] = mapped_column(default=0)


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
