from datetime import datetime
from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    title: str = Field(min_length=4, max_length=180)
    description: str = Field(min_length=10)
    category: str = "Geral"
    priority: str = "MEDIUM"

class TicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    assignee_id: int | None = None

class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

class CommentOutput(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime
    class Config:
        from_attributes = True

class TicketOutput(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: str
    status: str
    requester_id: int
    assignee_id: int | None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
