from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Destination
from schemas import BudgetRequest
from services.budget import plan_budget

router = APIRouter(prefix="/api/budget", tags=["Budget"])


@router.post("")
def budget_plan(req: BudgetRequest, db: Session = Depends(get_db)):
    dest = db.query(Destination).filter(Destination.id == req.destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    return plan_budget(dest, req)