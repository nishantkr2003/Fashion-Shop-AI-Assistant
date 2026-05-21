from pydantic import BaseModel

class ConversationCreate(BaseModel):
    title: str


class MessageInput(BaseModel):
    conversation_id: int
    content: str


class ChatResponse(BaseModel):
    message: str