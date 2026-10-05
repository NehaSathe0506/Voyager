from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Destination
from schemas import TripPreferences
from services.recommendation import recommend

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.post("")
def get_recommendations(prefs: TripPreferences, db: Session = Depends(get_db)):
    destinations = db.query(Destination).all()
    return recommend(destinations, prefs)