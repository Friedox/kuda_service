import datetime

from pydantic import BaseModel


class MessageScheme(BaseModel):
    chat_id: int
    user_id: int
    message: str
    timestamp: datetime.datetime


class MessageWithIdScheme(MessageScheme):
    message_id: int


class SendMessageScheme(MessageWithIdScheme):
    username: str
