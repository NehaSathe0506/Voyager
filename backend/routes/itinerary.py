from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Destination, Attraction
from schemas import ItineraryRequest
from services.itinerary import generate_itinerary

router = APIRouter(prefix="/api/itinerary", tags=["Itinerary"])


@router.post("")
def create_itinerary(req: ItineraryRequest, db: Session = Depends(get_db)):
    dest = db.query(Destination).filter(Destination.id == req.destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")

    attractions = db.query(Attraction).filter(Attraction.destination_id == dest.id).all()
    if not attractions:
        raise HTTPException(status_code=404, detail="No attractions added for this destination yet")

    return generate_itinerary(dest, attractions, req)