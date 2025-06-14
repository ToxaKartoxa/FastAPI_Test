import json

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

task_id = 0

def create_task():
    global task_id
    response = client.post(
#        "/tasks?name=000&description=0000" #,
        "/tasks",
        json={
            "name": "000",
            "description": "0000"
        },
    )
    assert response.status_code == 200
    # assert response.json() == {
    #     'ok': True,
    #     'task_id': 8
    # }
    jsn = response.json()
    assert jsn.get("task_id")
    assert jsn.get("ok")
    task_id = jsn.get("task_id")


def read_task():
    global task_id
    response = client.get("/tasks/id/" + str(task_id))
    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "name": "000",
        "description": "0000",
    }

def test_create_read_task():
    for i in range(0, 10):
        create_task()
        read_task()

# def test_read_nonexistent_item():
#     response = client.get("/items/10", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}