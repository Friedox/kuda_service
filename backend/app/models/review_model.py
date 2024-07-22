from sqlalchemy import Column, Integer, Float, String, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base


class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trip.trip_id"), nullable=False)

    score = Column(Integer, nullable=False)
    text = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint('score >= 0 AND score <= 5', name='check_score_range'),
        UniqueConstraint('user_id', 'trip_id', name='unique_user_trip_review')
    )
