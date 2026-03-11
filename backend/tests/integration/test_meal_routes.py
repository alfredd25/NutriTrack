from datetime import date


def test_create_meal(client):
    response = client.post(
        "/meals/create",
        json={"user_id": 1, "date": str(date.today()), "meal_type": "breakfast"},
    )
    assert response.status_code == 200


def test_get_day_summary_not_found(client):
    response = client.get("/meals/day-summary?user_id=999&date=2000-01-01")
    assert response.status_code == 404


def test_create_meal_invalid_meal_type(client):
    response = client.post(
        "/meals/create",
        json={"user_id": 1, "date": str(date.today()), "meal_type": "midnight_snack"},
    )
    assert response.status_code == 422


def test_create_meal_missing_fields(client):
    response = client.post("/meals/create", json={"user_id": 1})
    assert response.status_code == 422


def test_add_food_to_nonexistent_meal(client):
    response = client.post(
        "/meals/add-food", json={"meal_id": 99999, "food_id": 1, "quantity": 1.0}
    )
    assert response.status_code == 404


def test_add_food_negative_quantity(client):
    meal = client.post(
        "/meals/create",
        json={"user_id": 1, "date": str(date.today()), "meal_type": "lunch"},
    ).json()
    response = client.post(
        "/meals/add-food",
        json={"meal_id": meal["meal_id"], "food_id": 1, "quantity": -1.0},
    )
    assert response.status_code == 422


def test_add_food_zero_quantity(client):
    meal = client.post(
        "/meals/create",
        json={"user_id": 1, "date": str(date.today()), "meal_type": "dinner"},
    ).json()
    response = client.post(
        "/meals/add-food",
        json={"meal_id": meal["meal_id"], "food_id": 1, "quantity": 0.0},
    )
    assert response.status_code == 422


def test_day_summary_invalid_date_format(client):
    response = client.get("/meals/day-summary?user_id=1&date=not-a-date")
    assert response.status_code == 422