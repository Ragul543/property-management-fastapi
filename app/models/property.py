from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # land, residential, commercial
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    price = Column(Float, nullable=False)
    area_sqft = Column(Float, nullable=True)
    status = Column(String(50), default="available")  # available, sold, rented

    # Land-specific
    land_type = Column(String(100), nullable=True)
    soil_type = Column(String(100), nullable=True)
    road_access = Column(String(255), nullable=True)
    zoning = Column(String(100), nullable=True)

    # Residential-specific
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    floors = Column(Integer, nullable=True)
    furnishing = Column(String(50), nullable=True)  # furnished, semi, unfurnished
    parking = Column(String(100), nullable=True)
    amenities = Column(Text, nullable=True)

    # Commercial-specific
    commercial_type = Column(String(100), nullable=True)
    floor_number = Column(Integer, nullable=True)
    carpet_area = Column(Float, nullable=True)
    pantry = Column(Boolean, default=False)
    power_backup = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")


class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    property = relationship("Property", back_populates="images")
