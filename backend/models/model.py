from pydantic import BaseModel
from typing import List


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    document_text: str
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    content: str