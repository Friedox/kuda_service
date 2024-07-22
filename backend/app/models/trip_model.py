from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base


class Trip(Base):
    __tablename__ = "trip"
    trip_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pickup = Column(Integer, ForeignKey("point.point_id"), nullable=False)
    dropoff = Column(Integer, ForeignKey("point.point_id"), nullable=False)
    start_timestamp = Column(Integer, nullable=False)
    end_timestamp = Column(Integer, nullable=False)
    fare = Column(Integer, nullable=False)
    available_sits = Column(Integer, nullable=True)
    driver_phone = Column(String, nullable=True)
    driver_tg = Column(String, nullable=True)
    car_number = Column(String, nullable=True)
    car_type = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True)

    users = relationship("User", secondary="trip_user", back_populates="trips")
    tags = relationship("Tag", secondary="trip_tag", back_populates="trips")
