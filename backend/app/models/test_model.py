from sqlalchemy import Column, Integer, String

from models.base import Base


class Test(Base):
    __tablename__ = "test"
    test_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test = Column(String, nullable=False, unique=True)

