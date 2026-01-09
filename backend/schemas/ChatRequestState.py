# ChatRequest is external API data validation for FastAPI.
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None
