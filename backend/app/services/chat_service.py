from sqlalchemy import select
from app.models.conversation import (
    Conversation
)
from app.models.message import (
    Message
)




async def create_conversation(
    db,
    user_id,
    payload
):

    conversation = Conversation(
        user_id=user_id,
        title=payload.title
    )

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


async def save_message(
    db,
    conversation_id,
    role,
    content
):

    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg



async def get_history(
    db,
    conversation_id
):
    result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id)
    )

    return result.scalars().all()