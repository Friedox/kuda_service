from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base
from models.trip_model import car_trip_association

user_car_association = Table(
    'user_car', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True),
    Column('car_id', Integer, ForeignKey('car.car_id'), primary_key=True)
)


class Car(Base):
    __tablename__ = "car"
    car_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    model = Column(String, nullable=False)
    number = Column(String, nullable=False)
    region_number = Column(Integer, nullable=False)

    users = relationship("User", secondary=user_car_association, back_populates="cars")
    trips = relationship("Trip", secondary=car_trip_association, back_populates="cars")
