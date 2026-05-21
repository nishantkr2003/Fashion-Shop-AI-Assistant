from sqlalchemy import (
    select
)

from app.models.message import (
    Message
)


async def load_memory(db,conversation_id):

    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    )
    return (result.scalars().all())