from fastapi.testclient import TestClient

from fast_api.app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/", params={"token": "api-token"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}
