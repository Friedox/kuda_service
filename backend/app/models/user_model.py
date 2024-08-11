from sqlalchemy import Column, Integer, String, LargeBinary, Boolean
from sqlalchemy.orm import relationship

from models.base import Base
from models.car_model import user_car_association


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    telegram = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    password_hash = Column(LargeBinary)
    is_google_account = Column(Boolean, default=False)

    trips = relationship("Trip", secondary="trip_user", back_populates="users")
    cars = relationship("Car", secondary=user_car_association, back_populates="users")
