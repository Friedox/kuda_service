from sqlalchemy import Column, Integer, String

from models.base import Base


class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
