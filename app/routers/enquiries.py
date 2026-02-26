from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.enquiry import Enquiry
from app.models.property import Property
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate, EnquiryResponse

router = APIRouter(prefix="/enquiries", tags=["enquiries"])


def _to_response(enquiry: Enquiry) -> dict:
    data = {
        "id": enquiry.id,
        "property_id": enquiry.property_id,
        "name": enquiry.name,
        "email": enquiry.email,
        "phone": enquiry.phone,
        "message": enquiry.message,
        "status": enquiry.status,
        "created_at": enquiry.created_at,
        "updated_at": enquiry.updated_at,
        "property_title": enquiry.property.title if enquiry.property else None,
    }
    return data


@router.post("/", response_model=EnquiryResponse, status_code=201)
def create_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == enquiry.property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    db_enquiry = Enquiry(**enquiry.model_dump())
    db.add(db_enquiry)
    db.commit()
    db.refresh(db_enquiry)
    return _to_response(db_enquiry)


@router.get("/", response_model=List[EnquiryResponse])
def list_enquiries(
    property_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Enquiry)
    if property_id:
        query = query.filter(Enquiry.property_id == property_id)
    if status:
        query = query.filter(Enquiry.status == status)
    if search:
        query = query.filter(
            Enquiry.name.ilike(f"%{search}%")
            | Enquiry.email.ilike(f"%{search}%")
            | Enquiry.phone.ilike(f"%{search}%")
        )
    enquiries = query.order_by(Enquiry.created_at.desc()).all()
    return [_to_response(e) for e in enquiries]


@router.get("/{enquiry_id}", response_model=EnquiryResponse)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return _to_response(enquiry)


@router.put("/{enquiry_id}", response_model=EnquiryResponse)
def update_enquiry(enquiry_id: int, enquiry_update: EnquiryUpdate, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    update_data = enquiry_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(enquiry, key, value)
    db.commit()
    db.refresh(enquiry)
    return _to_response(enquiry)


@router.delete("/{enquiry_id}", status_code=204)
def delete_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    db.delete(enquiry)
    db.commit()
