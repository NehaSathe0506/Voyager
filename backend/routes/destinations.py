from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Destination

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

@router.get("/")
def list_destinations(db: Session = Depends(get_db)):
    return db.query(Destination).all()