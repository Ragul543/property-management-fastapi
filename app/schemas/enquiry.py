from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EnquiryCreate(BaseModel):
    property_id: int
    name: str
    email: str
    phone: str
    message: Optional[str] = None


class EnquiryUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None


class EnquiryResponse(BaseModel):
    id: int
    property_id: int
    name: str
    email: str
    phone: str
    message: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    property_title: Optional[str] = None

    class Config:
        from_attributes = True
