import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"

def test_version_check(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data

@pytest.mark.parametrize("route", ["/health", "/version"])
def test_routes_exist(client, route):
    response = client.get(route)
    assert response.status_code == 200

def test_version_with_monkeypatch(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "2.5.0")

    import app as flask_app
    monkeypatch.setattr(flask_app, "APP_VERSION", "2.5.0")

    response = client.get("/version")
    assert response.status_code == 200
    data = response.get_json()
    assert data["version"] == "2.5.0"