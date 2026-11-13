from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_strategy():
    """Test registering a new trading strategy via API endpoint."""
    response = client.post(
        "/strategies/",
        json={
            "name": "EMA Trend Follower",
            "symbol": "EURUSD",
            "timeframe": "1H",
            "is_active": True
        }
    )
    # Check if created successfully (201 Created or 200 OK depending on router config)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "EMA Trend Follower"
    assert data["symbol"] == "EURUSD"
    assert "id" in data

def test_get_strategies():
    """Test retrieving all registered trading strategies."""
    response = client.get("/strategies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)