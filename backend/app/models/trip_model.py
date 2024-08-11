from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Table
from sqlalchemy.orm import relationship
from models.base import Base

car_trip_association = Table(
    'car_trip', Base.metadata,
    Column('trip_id', Integer, ForeignKey('trip.trip_id'), primary_key=True),
    Column('car_id', Integer, ForeignKey('car.car_id'), primary_key=True)
)


class Trip(Base):
    __tablename__ = "trip"
    trip_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pickup = Column(Integer, ForeignKey("point.point_id"), nullable=False)
    dropoff = Column(Integer, ForeignKey("point.point_id"), nullable=False)
    start_timestamp = Column(Integer, nullable=False)
    end_timestamp = Column(Integer, nullable=False)
    fare = Column(Integer, nullable=False)
    available_sits = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=True)
    travel_time = Column(Float, nullable=True)

    users = relationship("User", secondary="trip_user", back_populates="trips")
    tags = relationship("Tag", secondary="trip_tag", back_populates="trips")
    cars = relationship("Car", secondary=car_trip_association, back_populates="trips")
