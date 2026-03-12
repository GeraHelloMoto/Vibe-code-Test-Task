from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from app import models, schemas
from app.database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{master_id}/requests", response_model=List[schemas.Request])
def get_my_requests(master_id: int, db: Session = Depends(get_db)):
    master = db.query(models.User).filter(models.User.id == master_id, models.User.role == "master").first()
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    requests = db.query(models.Request).filter(models.Request.assignedTo == master_id).all()
    return requests

@router.patch("/requests/{request_id}/take")
def take_request(request_id: int, master_id: int, db: Session = Depends(get_db)):
    stmt = update(models.Request).where(
        models.Request.id == request_id,
        models.Request.status == "assigned",
        models.Request.assignedTo == master_id
    ).values(status="in_progress")
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        req = db.query(models.Request).filter(models.Request.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        if req.assignedTo != master_id:
            raise HTTPException(status_code=403, detail="This request is not assigned to you")
        if req.status != "assigned":
            raise HTTPException(status_code=409, detail=f"Request cannot be taken because status is {req.status}")
        raise HTTPException(status_code=409, detail="Request was already taken by another master")
    return {"message": "Request taken successfully"}

@router.patch("/requests/{request_id}/complete")
def complete_request(request_id: int, master_id: int, db: Session = Depends(get_db)):
    request = db.query(models.Request).filter(
        models.Request.id == request_id,
        models.Request.assignedTo == master_id,
        models.Request.status == "in_progress"
    ).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found or not in progress")
    request.status = "done"
    db.commit()
    return {"message": "Request completed successfully"}