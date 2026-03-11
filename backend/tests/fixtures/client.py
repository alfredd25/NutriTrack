import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    from app.api.food import get_db
    from app.api.meal import get_db as meal_get_db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[meal_get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
