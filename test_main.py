from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks",
        json={"name": "000", "description": "0000"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "000",
        "description": "0000",
    }

def test_read_task():
    response = client.get("/tasks/id/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "111",
        "description": "1111",
    }

# def test_read_nonexistent_item():
#     response = client.get("/items/10", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}