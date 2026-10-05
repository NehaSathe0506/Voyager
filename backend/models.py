from sqlalchemy import Column, Integer, String, Text, Numeric, Float
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