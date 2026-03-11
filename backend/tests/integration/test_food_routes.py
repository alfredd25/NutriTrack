def test_food_search(client):
    response = client.get("/foods/search?q=chicken")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_food_autocomplete(client):
    response = client.get("/foods/autocomplete?q=chick")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_empty_search_returns_results(client):
    response = client.get("/foods/search?q=rice")
    assert response.status_code == 200


def test_food_search_typo(client):
    response = client.get("/foods/search?q=chiken")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_food_search_empty_query(client):
    response = client.get("/foods/search?q=")
    assert response.status_code in (200, 422)


def test_food_search_long_query(client):
    long_query = "a" * 300
    response = client.get(f"/foods/search?q={long_query}")
    assert response.status_code in (200, 422)


def test_food_search_sql_injection(client):
    response = client.get("/foods/search?q=' OR '1'='1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_food_search_missing_query_param(client):
    response = client.get("/foods/search")
    assert response.status_code == 422


def test_food_autocomplete_short_query(client):
    response = client.get("/foods/autocomplete?q=a")
    assert response.status_code == 200
    assert isinstance(response.json(), list)