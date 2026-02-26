import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.property import Property, PropertyImage
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "properties")

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(prop: PropertyCreate, db: Session = Depends(get_db)):
    db_prop = Property(**prop.model_dump())
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop


@router.get("/", response_model=List[PropertyResponse])
def list_properties(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Property)
    if category:
        query = query.filter(Property.category == category)
    if status:
        query = query.filter(Property.status == status)
    if search:
        query = query.filter(
            Property.title.ilike(f"%{search}%")
            | Property.city.ilike(f"%{search}%")
            | Property.address.ilike(f"%{search}%")
        )
    return query.order_by(Property.created_at.desc()).all()


@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, prop_update: PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    update_data = prop_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prop, key, value)
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/{property_id}", status_code=204)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    # Delete image files from disk
    for img in prop.images:
        file_path = os.path.join(UPLOAD_DIR, os.path.basename(img.image_path))
        if os.path.exists(file_path):
            os.remove(file_path)
    db.delete(prop)
    db.commit()


@router.post("/{property_id}/images", response_model=List[dict])
def upload_images(
    property_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    uploaded = []
    has_primary = db.query(PropertyImage).filter(
        PropertyImage.property_id == property_id, PropertyImage.is_primary == True
    ).first() is not None

    for i, file in enumerate(files):
        ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        is_primary = not has_primary and i == 0
        db_image = PropertyImage(
            property_id=property_id,
            image_path=f"/uploads/properties/{filename}",
            is_primary=is_primary,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        uploaded.append({
            "id": db_image.id,
            "image_path": db_image.image_path,
            "is_primary": db_image.is_primary,
        })
        if is_primary:
            has_primary = True

    return uploaded


@router.delete("/{property_id}/images/{image_id}", status_code=204)
def delete_image(property_id: int, image_id: int, db: Session = Depends(get_db)):
    image = db.query(PropertyImage).filter(
        PropertyImage.id == image_id, PropertyImage.property_id == property_id
    ).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    file_path = os.path.join(UPLOAD_DIR, os.path.basename(image.image_path))
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(image)
    db.commit()
