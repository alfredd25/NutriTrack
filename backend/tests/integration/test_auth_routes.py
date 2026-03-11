def test_register_user(client):
    response = client.post(
        "/auth/register", json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_login_user(client):
    client.post(
        "/auth/register", json={"email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/login", json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200


def test_duplicate_register_fails(client):
    client.post(
        "/auth/register", json={"email": "dup@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/register", json={"email": "dup@example.com", "password": "password123"}
    )
    assert response.status_code == 400


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": "correctpassword"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login", json={"email": "ghost@example.com", "password": "password123"}
    )
    assert response.status_code == 401


def test_register_missing_email(client):
    response = client.post("/auth/register", json={"password": "password123"})
    assert response.status_code == 422


def test_register_missing_password(client):
    response = client.post("/auth/register", json={"email": "nopass@example.com"})
    assert response.status_code == 422


def test_register_invalid_email_format(client):
    response = client.post(
        "/auth/register", json={"email": "not-an-email", "password": "password123"}
    )
    assert response.status_code == 422