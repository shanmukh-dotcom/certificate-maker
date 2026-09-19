from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.models import EventStatus

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    issue_date: Optional[datetime] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    status: Optional[EventStatus] = None

class EventOut(EventBase):
    id: int
    organization_id: int
    status: EventStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
