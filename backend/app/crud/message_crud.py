from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models import Message
from schemas.message_scheme import MessageScheme, MessageWithIdScheme


async def save_message(message: MessageScheme, db: AsyncSession) -> MessageWithIdScheme:
    new_message = Message(
        chat_id=message.chat_id,
        user_id=message.user_id,
        message=message.message,
        timestamp=message.timestamp
    )

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    message_scheme = MessageWithIdScheme(**new_message.__dict__)
    return message_scheme


async def get_chat_messages(
        db: AsyncSession,
        chat_id: int,
        limit: int = 100,
        offset: int = 0
) -> list[MessageWithIdScheme]:
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    messages = result.scalars().all()

    message_schemas = [MessageWithIdScheme(**message.__dict__) for message in messages]

    return message_schemas
