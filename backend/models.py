from sqlalchemy import Column, Integer, String, Text, Numeric, Float
from sqlalchemy import Column, Integer, String, Text, Numeric, Float, Boolean, ForeignKey
from database import Base

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    state = Column(String(100))
    country = Column(String(100), default="India")
    description = Column(Text)
    average_budget_per_day = Column(Numeric(10, 2))
    best_months = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    nature_score = Column(Integer, default=5)
    adventure_score = Column(Integer, default=5)
    culture_score = Column(Integer, default=5)
    nightlife_score = Column(Integer, default=5)
    relaxation_score = Column(Integer, default=5)

class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(30))          # nature, adventure, culture, nightlife, relaxation
    latitude = Column(Float)
    longitude = Column(Float)
    duration_hours = Column(Float, default=2)
    cost = Column(Numeric(10, 2), default=0)   # INR per person
    outdoor = Column(Boolean, default=True)