from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base


class TripTag(Base):
    __tablename__ = "trip_tag"
    trip_tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("tag.tag_id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trip.trip_id"), nullable=False)
