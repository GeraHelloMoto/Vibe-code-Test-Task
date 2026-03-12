from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/requests", response_model=List[schemas.Request])
def list_all_requests(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Request)
    if status:
        query = query.filter(models.Request.status == status)
    return query.all()

@router.patch("/requests/{request_id}/assign")
def assign_master(request_id: int, master_id: int, db: Session = Depends(get_db)):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    master = db.query(models.User).filter(models.User.id == master_id, models.User.role == "master").first()
    if not master:
        raise HTTPException(status_code=400, detail="Invalid master id")
    if request.status not in ["new", "assigned"]:
        raise HTTPException(status_code=400, detail="Cannot assign request in current status")
    request.assignedTo = master_id
    request.status = "assigned"
    db.commit()
    return {"message": "Assigned successfully"}

@router.patch("/requests/{request_id}/cancel")
def cancel_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    if request.status in ["done", "canceled"]:
        raise HTTPException(status_code=400, detail="Cannot cancel request in current status")
    request.status = "canceled"
    db.commit()
    return {"message": "Canceled successfully"}