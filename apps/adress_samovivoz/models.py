from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class AdressSamovivoz(Base):
#     __tablename__ = "adress_samovivoz"
#
#     id = Column(Integer, primary_key=True, index=True)
#     adress = Column(String, nullable=False, unique=True)