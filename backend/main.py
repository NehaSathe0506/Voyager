from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import destinations, recommendations
import models  # noqa: F401
from routes import destinations

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Voyager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(destinations.router)
app.include_router(recommendations.router)

@app.get("/")
def home():
    return {"message": "Voyager API is running"}