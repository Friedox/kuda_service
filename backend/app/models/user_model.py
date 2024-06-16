from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(LargeBinary, nullable=False)

    trips = relationship("Trip", secondary="trip_user", back_populates="users")
