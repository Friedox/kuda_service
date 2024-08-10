from sqlalchemy import Column, Integer, String

from models.base import Base


class Car(Base):
    __tablename__ = "car"
    car_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    model = Column(String, nullable=False)
    number = Column(String, nullable=False)
    region_number = Column(Integer, nullable=False)
