import uuid
from http.cookiejar import debug

from fastapi.testclient import TestClient

from src.main import app

import pytest

from src.repository import TaskRepository
from src.schemas import STaskAdd, STaskID

client = TestClient(app)




# Тест на удаление всех тасок и чтение на проверку
def test_del_read_tasks():
    print('\nОчистка БД')
    del_tasks()
    print('Проверка БД на очистку')
    read_tasks()


# Тест на удаление всех тасок
def del_tasks():
    response = client.delete("/tasks")
    assert response.status_code == 200
    jsn = response.json()
    assert jsn.get("ok") == 'Все таски уничтожены'


# Тест на чтение всех тасок после удаления
def read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

############################################################

@pytest.fixture(scope="function")
async def cr_tasks():
    task = STaskAdd(name="task", description="<UNK> <UNK> <UNK>")
    task_id = await TaskRepository.add_one(task)
    return STaskID(ok=True, task_id=task_id)


@pytest.fixture(scope="function")
def cr_tasks2():
    # print(str(uuid.uuid4())+'111')
    # breakpoint()
    print("\nРаз")
    yield
    print("\nДва")
    # print(str(uuid.uuid4())+'222')

############################################################


# Тест на запись, правку, проверку и удаление тасок по id и порядковому номеру
def test_create_read_put_del_tasks(cr_tasks2):
    create_read_put_del_tasks(100, 'id')
    create_read_put_del_tasks(100, 'N')


def create_read_put_del_tasks(task_n: int, N_id: str):
    # print('\n')
    print('Запись-чтение тасок по ' + N_id + ', n = 1 до ' + str(task_n))
    for i in range(1, task_n+1):
        create_task(i, 'name', 'description')
        read_task(N_id, i, 'name', 'description', True)

    print('Чтение всех тасок разом по ' + N_id + ', n = 1 до ' + str(task_n))
    read_tasks_series(1, task_n, 'name', 'description')

    print('Обновление-чтение тасок по ' + N_id + ', n = 1 до ' + str(task_n))
    for i in range(1, task_n+1):
        put_task(N_id, i, 'имя', 'дескриптор', True)
        read_task(N_id, i, 'имя', 'дескриптор', True)

    print('Обновление-чтение-удаление не существующих тасок по ' + N_id + ', n = ' + str(task_n) + ' до ' + str(task_n*2-1))
    for i in range(task_n+1, task_n*2):
        put_task(N_id, i, '', '', False)
        read_task(N_id, i, '', '', False)
        del_task(N_id, i, False)

    print('Обновление-чтение-удаление не существующих тасок по ' + N_id + ', n = 0 до ' + str(-task_n))
    for i in range(0, -task_n-1, -1):
        put_task(N_id, i, '', '', False)
        read_task(N_id, i, '', '', False)
        del_task(N_id, i, False)

    print('Удаление тасок по ' + N_id + ', n = 1 до ' + str(task_n))
    for i in range(task_n, 0, -1):
        del_task(N_id, i, True)

    print('Проверка БД на очистку')
    read_tasks()


# Тест на запись таски
# @pytest.fixture(scope="function")
def create_task(task_id: int, name: str, description: str) -> int:
    response = client.post(
#        "/tasks?name=000&description=0000" #,
        "/tasks/json",
        json={
            "name": name + str(task_id),
            "description": description + str(task_id)
        },
    )
    assert response.status_code == 200
    jsn = response.json()
    assert jsn.get("task_id")
    assert jsn.get("ok")
    return jsn.get("task_id")


# Тест на чтение таски
def read_task(N_id: str, task_id: int, name: str, description: str, err: bool):
    response = client.get("/tasks/" + N_id + "/" + str(task_id))
    if err:
        assert response.status_code == 200
        assert response.json() == {
            "id": task_id,
            "name": name + str(task_id),
            "description": description + str(task_id)
        }
    else:
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Таска не найдена"
        }


# Тест на замену существующей таску по id
def put_task(N_id: str, task_id: int, name: str, description: str, err: bool):
    response = client.put(
        url="/tasks/" + N_id + "/json/" + str(task_id),
        json={
            "name": name + str(task_id),
            "description": description + str(task_id)
        },
    )
    if err:
        assert response.status_code == 200
        if N_id != "id":
            N_id = "порядковому номеру"
        assert response.json() == [
            {
                "ok": "Таска успешно заменена по " + N_id
            },
            {
                "name": name + str(task_id),
                "description": description + str(task_id),
                "id": task_id
            }
        ]
    else:
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Таска не найдена"
        }


# Тест на удаление таски
def del_task(N_id: str, task_id: int, err: bool):
    response = client.delete("/tasks/" + N_id + "/" + str(task_id))
    if err:
        assert response.status_code == 200
        if N_id != "id":
            N_id = "порядковому номеру"
        assert response.json() == {
                "ok": "Таска уничтожена по " + N_id
            }
    else:
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Таска не найдена"
        }


# Тест на чтение всех созданных тасок
def read_tasks_series(start: int, iteration: int, name: str, description: str):
    response = client.get("/tasks")
    assert response.status_code == 200
    data_jsn = response.json()
    # Создаем словарь, где ключи - это id, а значения - соответствующие объекты
    jsn = {item["id"]: item for item in data_jsn}
    # В цикле перебираем таски
    for task_id in range(start, iteration+1):
        target_object = jsn.get(task_id)  # Получаем объект по id
        assert target_object == {
            "id": task_id,
            "name": name + str(task_id),
            "description": description + str(task_id)
        }


############################################################

def test_read_files():
    print('\nЧтение файла иконки')
    read_file("/favicon.ico", "./favicon.ico", 'image/x-icon')
    print('Чтение файла видоса')
    read_file("/Santex_download_1", "./Santex.mp4", 'video/mp4')


def read_file(url: str, path: str, ContentType: str):
    response = client.get(url)
    assert response.status_code == 200
    # Проверяем тип контента
    assert response.headers['Content-Type'] == ContentType  # Замените на нужный тип
    # Проверяем содержимое
    with open(path, mode="rb") as f:
        expected_content = f.read()
        assert response.content == expected_content
    print(response.headers)
