from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    db_request = models.Request(**request.dict(), status="new")
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/", response_model=List[schemas.Request])
def list_requests(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Request)
    if status:
        query = query.filter(models.Request.status == status)
    return query.all()