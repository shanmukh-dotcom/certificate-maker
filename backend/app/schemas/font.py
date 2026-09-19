from pydantic import BaseModel
from datetime import datetime

class FontOut(BaseModel):
    id: int
    name: str
    format: str
    created_at: datetime
    
    class Config:
        from_attributes = True
