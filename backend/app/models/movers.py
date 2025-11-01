from sqlalchemy import Column, Integer, String, Float
from ..db.database import Base


class Mover(Base):
    """이삿짐 센터 모델"""
    __tablename__ = "movers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, index=True, nullable=False)
    phone = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
