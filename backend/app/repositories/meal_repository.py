from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.meal import Meal
from app.models.meal_item import MealItem
from app.models.daily_summary import DailySummary


def create_meal(db: Session, user_id: int, date, meal_type: str):
    existing_meal = (
        db.query(Meal)
        .filter_by(user_id=user_id, date=date, meal_type=meal_type)
        .first()
    )

    if existing_meal:
        return existing_meal

    meal = Meal(user_id=user_id, date=date, meal_type=meal_type)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


def add_meal_item(db: Session, meal_id: int, food, quantity: float):
    meal_item = MealItem(
        meal_id=meal_id,
        food_id=food.id,
        quantity=quantity,
        calories=food.calories * quantity,
        protein=food.protein * quantity,
        carbs=food.carbs * quantity,
        fat=food.fat * quantity,
    )
    db.add(meal_item)
    db.commit()
    return meal_item


def update_daily_summary(db: Session, user_id: int, date):
    totals = db.execute(
        text("""
        SELECT
            SUM(mi.calories) as calories,
            SUM(mi.protein) as protein,
            SUM(mi.carbs) as carbs,
            SUM(mi.fat) as fat
        FROM meal_items mi
        JOIN meals m ON mi.meal_id = m.id
        WHERE m.user_id = :user_id
        AND m.date = :date
    """),
        {"user_id": user_id, "date": date},
    ).fetchone()

    existing = db.query(DailySummary).filter_by(user_id=user_id, date=date).first()

    if existing:
        existing.calories = totals.calories or 0
        existing.protein = totals.protein or 0
        existing.carbs = totals.carbs or 0
        existing.fat = totals.fat or 0
    else:
        summary = DailySummary(
            user_id=user_id,
            date=date,
            calories=totals.calories or 0,
            protein=totals.protein or 0,
            carbs=totals.carbs or 0,
            fat=totals.fat or 0,
        )
        db.add(summary)

    db.commit()

def remove_meal_item(db: Session, meal_item_id: int, user_id: int):
    meal_item = db.query(MealItem).filter(MealItem.id == meal_item_id).first()
    if not meal_item:
        return None
    
    meal = db.query(Meal).filter(Meal.id == meal_item.meal_id).first()
    if meal.user_id != user_id:
        return None
    
    date = meal.date
    db.delete(meal_item)
    db.commit()
    update_daily_summary(db, user_id, date)
    return True


def get_weekly_summary(db: Session, user_id: int):
    rows = db.execute(
        text("""
        SELECT date, calories, protein, carbs, fat
        FROM daily_summaries
        WHERE user_id = :user_id
        AND date >= CURRENT_DATE - INTERVAL '6 days'
        ORDER BY date ASC
    """),
        {"user_id": user_id},
    ).fetchall()
    return rows


def get_streak(db: Session, user_id: int):
    rows = db.execute(
        text("""
        SELECT date FROM daily_summaries
        WHERE user_id = :user_id
        AND calories > 0
        ORDER BY date DESC
    """),
        {"user_id": user_id},
    ).fetchall()

    if not rows:
        return 0

    from datetime import date, timedelta
    streak = 0
    expected = date.today()

    for row in rows:
        if row.date == expected:
            streak += 1
            expected -= timedelta(days=1)
        else:
            break

    return streak