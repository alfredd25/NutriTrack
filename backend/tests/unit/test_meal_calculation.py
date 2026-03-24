from unittest.mock import MagicMock

from app.repositories.meal_repository import add_meal_item


def test_macro_calculation_100g():
    """100g of chicken (165 cal/100g) should give exactly the per-100g values."""
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 165.0
    food.protein = 31.0
    food.carbs = 0.0
    food.fat = 3.6
    quantity = 100.0  # 100g
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 165.0
    assert added.protein == 31.0
    assert added.fat == 3.6


def test_macro_calculation_200g():
    """200g should double the per-100g values."""
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 165.0
    food.protein = 31.0
    food.carbs = 0.0
    food.fat = 3.6
    quantity = 200.0  # 200g
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 330.0
    assert added.protein == 62.0
    assert added.fat == 7.2


def test_macro_calculation_50g():
    """50g should give half the per-100g values."""
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 100.0
    food.protein = 10.0
    food.carbs = 20.0
    food.fat = 5.0
    quantity = 50.0  # 50g
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 50.0
    assert added.protein == 5.0
    assert added.carbs == 10.0
    assert added.fat == 2.5


def test_macro_calculation_rounding():
    """300g should correctly scale per-100g values with decimals."""
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 100.0
    food.protein = 10.0
    food.carbs = 20.0
    food.fat = 3.3
    quantity = 300.0  # 300g
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 300.0
    assert abs(added.fat - 9.9) < 0.01


def test_macro_calculation_large_quantity():
    """500g should give 5x the per-100g values."""
    mock_db = MagicMock()
    food = MagicMock()
    food.id = 1
    food.calories = 50.0
    food.protein = 5.0
    food.carbs = 8.0
    food.fat = 1.0
    quantity = 500.0  # 500g
    add_meal_item(mock_db, meal_id=1, food=food, quantity=quantity)
    added = mock_db.add.call_args[0][0]
    assert added.calories == 250.0
    assert added.protein == 25.0