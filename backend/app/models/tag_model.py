from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Tag(Base):
    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag = Column(String, nullable=False, unique=True)

    trips = relationship("Trip", secondary="trip_tag", back_populates="tags")
