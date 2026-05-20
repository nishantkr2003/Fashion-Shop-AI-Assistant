from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import StreamingResponse

from sqlalchemy import select

import asyncio

from app.db.database import get_db

from fastapi.responses import (
    StreamingResponse
)
from app.middleware.auth import (
    get_current_user
)

from app.schemas.chat_schema import (
    ConversationCreate,
    MessageInput
)

from app.services.chat_service import (
    create_conversation,
    save_message,
    get_history
)

from app.services.title_service import (
    generate_title
)

from app.models.conversation import (
    Conversation
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# CREATE CONVERSATION

@router.post(
    "/conversation",
    operation_id="create_conversation"
)
async def new_chat(
    payload: ConversationCreate,
    db=Depends(get_db),
    user_id=Depends(get_current_user)

):
    try:
        conversation = await create_conversation(
            db,
            user_id,
            payload
)

        return {
            "id":conversation.id,
            "title":conversation.title
        }
    except Exception as e:
        raise HTTPException(400,str(e))


# SEND MESSAGE

@router.post(
    "/message",
    operation_id="send_message"
)
async def send_message(
    payload: MessageInput,
    db=Depends(get_db)

):

    try:
        conversation = await db.get(
            Conversation,
            payload.conversation_id
        )

        if not conversation:
            raise HTTPException(404,"Conversation not found")

        if conversation.title == "New Chat":
            title = await generate_title(
                payload.content
            )
            conversation.title = title
            await db.commit()

        await save_message(
            db,
            payload.conversation_id,
            "user",payload.content
        )
        reply = ("This is temporary AI response")
        await save_message(
            db,
            payload.conversation_id,
            "assistant",reply
        )

        return {"reply":reply}

    except Exception as e:
        raise HTTPException(400,str(e))


# STREAM RESPONSE

@router.post(
    "/stream",
    operation_id="stream_chat"
)

async def stream(
    payload: MessageInput,
    db=Depends(get_db)

):
    async def generate():
        await save_message(
            db,
            payload.conversation_id,
            "user",payload.content
        )

        conversation = await db.get(
        Conversation,
        payload.conversation_id
        )

        if ( conversation and conversation.title == "New Chat"):
            title = await generate_title(
                payload.content
            )
            conversation.title = title
            await db.commit()

        reply = ("Temporary streamed AI response")
        streamed = ""
        for ch in reply:
            streamed += ch
            yield(ch.encode("utf-8"))
            await asyncio.sleep(0.05)

        await save_message(
            db,
            payload.conversation_id,
            "assistant",
            streamed
        )

    return StreamingResponse(
        generate(),

        media_type="text/event-stream",
         headers={
            "Cache-Control":"no-cache",
            "Connection":"keep-alive"

        }
    )

# GET CHAT HISTORY

@router.get(
    "/history/{conversation_id}",
    operation_id="chat_history"
)
async def history(
    conversation_id: int,
    db=Depends(get_db)
):
    try:
        messages = await get_history(
            db,
            conversation_id
        )
        return [
            {
                "id":m.id,
                "role":m.role,
                "content":m.content,
                "created_at":m.created_at
            }
            for m in messages
        ]

    except Exception as e:
        raise HTTPException(400,str(e))


# SIDEBAR CONVERSATIONS

@router.get(
    "/conversations",
    operation_id="list_conversations"
)
async def conversations(
    db=Depends(get_db),
    user_id=Depends(get_current_user)

):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
    )
    data = result.scalars().all()

    return [
        {
            "id":c.id,
            "title":c.title,
            "created_at":c.created_at
        }
        for c in data
    ]


