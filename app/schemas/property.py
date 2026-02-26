from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PropertyImageResponse(BaseModel):
    id: int
    property_id: int
    image_path: str
    is_primary: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PropertyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    price: float
    area_sqft: Optional[float] = None
    status: Optional[str] = "available"

    # Land-specific
    land_type: Optional[str] = None
    soil_type: Optional[str] = None
    road_access: Optional[str] = None
    zoning: Optional[str] = None

    # Residential-specific
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floors: Optional[int] = None
    furnishing: Optional[str] = None
    parking: Optional[str] = None
    amenities: Optional[str] = None

    # Commercial-specific
    commercial_type: Optional[str] = None
    floor_number: Optional[int] = None
    carpet_area: Optional[float] = None
    pantry: Optional[bool] = False
    power_backup: Optional[bool] = False


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    price: Optional[float] = None
    area_sqft: Optional[float] = None
    status: Optional[str] = None

    land_type: Optional[str] = None
    soil_type: Optional[str] = None
    road_access: Optional[str] = None
    zoning: Optional[str] = None

    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floors: Optional[int] = None
    furnishing: Optional[str] = None
    parking: Optional[str] = None
    amenities: Optional[str] = None

    commercial_type: Optional[str] = None
    floor_number: Optional[int] = None
    carpet_area: Optional[float] = None
    pantry: Optional[bool] = None
    power_backup: Optional[bool] = None


class PropertyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    price: float
    area_sqft: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    land_type: Optional[str] = None
    soil_type: Optional[str] = None
    road_access: Optional[str] = None
    zoning: Optional[str] = None

    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floors: Optional[int] = None
    furnishing: Optional[str] = None
    parking: Optional[str] = None
    amenities: Optional[str] = None

    commercial_type: Optional[str] = None
    floor_number: Optional[int] = None
    carpet_area: Optional[float] = None
    pantry: Optional[bool] = None
    power_backup: Optional[bool] = None

    images: List[PropertyImageResponse] = []

    class Config:
        from_attributes = True
