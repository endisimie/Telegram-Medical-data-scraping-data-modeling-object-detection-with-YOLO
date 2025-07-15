from pydantic import BaseModel
from typing import List, Optional

class ProductReport(BaseModel):
    product: str
    mentions: int

class ChannelActivity(BaseModel):
    channel: str
    total_messages: int
    avg_message_length: float

class MessageSearchResult(BaseModel):
    message_id: int
    channel: str
    message_text: str
    timestamp: str
