from unittest.mock import MagicMock

from app.repositories.meal_repository import add_meal_item


def test_macro_calculation():
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 165.0
    food.protein = 31.0
    food.carbs = 0.0
    food.fat = 3.6
    quantity = 2.0
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 330.0
    assert added.protein == 62.0
    assert added.fat == 7.2


def test_macro_calculation_decimal_quantity():
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 100.0
    food.protein = 10.0
    food.carbs = 20.0
    food.fat = 5.0
    quantity = 0.5
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 50.0
    assert added.protein == 5.0
    assert added.carbs == 10.0
    assert added.fat == 2.5


def test_macro_calculation_rounding():
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 100.0
    food.protein = 10.0
    food.carbs = 20.0
    food.fat = 3.3
    quantity = 3.0
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 300.0
    assert abs(added.fat - 9.9) < 0.01


def test_macro_calculation_large_quantity():
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 50.0
    food.protein = 5.0
    food.carbs = 8.0
    food.fat = 1.0
    quantity = 100.0
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 5000.0
    assert added.protein == 500.0