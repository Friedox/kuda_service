from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Trip(Base):
    __tablename__ = "trip"
    trip_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pickup = Column(String, nullable=False)
    dropoff = Column(String, nullable=False)
    start_timestamp = Column(String, nullable=False)
    end_timestamp = Column(String, nullable=False)
    fare = Column(Integer, nullable=False)

    users = relationship("User", secondary="trip_user", back_populates="trips")
    tags = relationship("Tag", secondary="trip_tag", back_populates="trips")
