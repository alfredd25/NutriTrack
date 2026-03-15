from sqlalchemy import text
from sqlalchemy.orm import Session


def search_foods(db: Session, query: str):
    sql = text("""
        SELECT id, name, calories, protein, carbs, fat
        FROM foods
        WHERE search_vector @@ websearch_to_tsquery('english', :query)
        ORDER BY ts_rank(search_vector, websearch_to_tsquery('english', :query)) DESC
        LIMIT 10
    """)
    result = db.execute(sql, {"query": query})
    return result.fetchall()


def search_foods_trigram(db: Session, query: str):
    sql = text("""
        SELECT id, name, calories, protein, carbs, fat
        FROM foods
        WHERE name % :query
        ORDER BY similarity(name, :query) DESC
        LIMIT 10
    """)
    result = db.execute(sql, {"query": query})
    return result.fetchall()


def autocomplete_foods(db: Session, query: str):
    words = query.strip().split()
    conditions = " AND ".join([f"name ILIKE :word{i}" for i in range(len(words))])
    
    sql = text(f"""
        SELECT id, name, calories, protein, carbs, fat
        FROM foods
        WHERE {conditions}
        ORDER BY name
        LIMIT 10
    """)
    
    params = {f"word{i}": f"%{word}%" for i, word in enumerate(words)}
    result = db.execute(sql, params)
    return result.fetchall()


def get_food_by_id(db: Session, food_id: int):
    from app.models.food import Food
    return db.query(Food).filter(Food.id == food_id).first()