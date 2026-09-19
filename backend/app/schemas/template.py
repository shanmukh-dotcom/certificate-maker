from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class TemplateBase(BaseModel):
    name: str

class TemplateCreate(TemplateBase):
    pass

class TemplateOut(TemplateBase):
    id: int
    organization_id: int
    base_image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TemplateVersionCreate(BaseModel):
    configuration: Any

class TemplateVersionOut(BaseModel):
    id: int
    template_id: int
    version_number: int
    configuration: Any
    created_at: datetime

    class Config:
        from_attributes = True
