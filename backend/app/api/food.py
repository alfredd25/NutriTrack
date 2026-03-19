from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.food_service import search_food, autocomplete_food
from app.auth.jwt_handler import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/foods/search")
def search_food_endpoint(
    q: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    return search_food(db, q)


@router.get("/foods/autocomplete")
def autocomplete_endpoint(
    q: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    return autocomplete_food(db, q)