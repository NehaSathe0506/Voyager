from typing import List, Literal
from pydantic import BaseModel, Field


class TripPreferences(BaseModel):
    start_city: str = "Mumbai"
    budget: float = Field(gt=0)                 # per person, whole trip (INR)
    days: int = Field(ge=1, le=30)
    travelers: int = Field(default=1, ge=1, le=20)
    month: str = "Dec"                          # Jan, Feb, ... Dec
    interests: List[str] = []                   # nature, adventure, culture, nightlife, relaxation
    travel_style: Literal["budget", "standard", "luxury"] = "budget"


class BudgetRequest(BaseModel):
    destination_id: int
    start_city: str = "Mumbai"
    budget: float = Field(gt=0)                 # per person, whole trip (INR)
    days: int = Field(ge=1, le=30)
    travel_style: Literal["budget", "standard", "luxury"] = "budget"