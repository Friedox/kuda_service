from sqlalchemy import Column, Integer, Float

from ..database import Base


class Point(Base):
    __tablename__ = "point"
    point_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
