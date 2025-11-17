from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey,
    Numeric, Boolean, Enum, Text
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    price = Column(Numeric(10, 2), nullable=False)
    img_url = Column(String(250))
