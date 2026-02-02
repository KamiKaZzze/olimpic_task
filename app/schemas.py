from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    user_input: str
    chat_history: List[dict]
