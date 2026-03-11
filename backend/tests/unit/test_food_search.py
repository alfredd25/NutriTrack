from unittest.mock import MagicMock, patch
from app.services.food_service import search_food


def test_search_returns_cached_result():
    mock_db = MagicMock()

    with patch("app.services.food_service.redis_client") as mock_redis:
        mock_redis.get.return_value = '[{"id": 1, "name": "Chicken", "calories": 200, "protein": 30, "carbs": 0, "fat": 5}]'
        result = search_food(mock_db, "chicken")
        assert len(result) == 1
        assert result[0]["name"] == "Chicken"
        mock_db.execute.assert_not_called()


def test_search_queries_db_on_cache_miss():
    mock_db = MagicMock()
    mock_row = MagicMock()
    mock_row.id = 1
    mock_row.name = "Chicken Breast"
    mock_row.calories = 165
    mock_row.protein = 31
    mock_row.carbs = 0
    mock_row.fat = 3.6

    with patch("app.services.food_service.redis_client") as mock_redis:
        mock_redis.get.return_value = None
        with patch("app.services.food_service.search_foods") as mock_search:
            mock_search.return_value = [mock_row]
            result = search_food(mock_db, "chicken")
            assert len(result) == 1
            assert result[0]["name"] == "Chicken Breast"
