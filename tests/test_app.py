import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball Club" in data
    assert isinstance(data["Basketball Club"], dict)

def test_signup_for_activity():
    response = client.post("/activities/Basketball Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Basketball Club" in response.json()["message"]
    # Try signing up again (should fail)
    response = client.post("/activities/Basketball Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 400

def test_unregister_from_activity():
    # First, sign up
    client.post("/activities/Tennis Team/signup", params={"email": "removeuser@mergington.edu"})
    # Now, unregister
    response = client.post("/activities/Tennis Team/unregister", params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 200
    assert "Removed removeuser@mergington.edu from Tennis Team" in response.json()["message"]
    # Try unregistering again (should fail)
    response = client.post("/activities/Tennis Team/unregister", params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 404
