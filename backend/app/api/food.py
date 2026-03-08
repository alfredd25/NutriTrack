from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.food_service import search_food, autocomplete_food

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/foods/search")
def search_food_endpoint(q: str, db: Session = Depends(get_db)):
    return search_food(db, q)

@router.get("/foods/autocomplete")
def autocomplete(q: str, db: Session = Depends(get_db)):
    return autocomplete_food(db, q)