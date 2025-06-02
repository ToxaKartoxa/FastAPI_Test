from typing import Annotated, Any, Coroutine

from OAuth2 import authenticate_user, fake_users_db, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token
from database import delete_tables, create_tables
from repository import TaskRepository
from schemas import STaskAdd, STask, STaskID, Token, User

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends, HTTPException, status, APIRouter, Response
from datetime import timedelta

from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse

import os


router = APIRouter(
#    prefix="/tasks",
    tags=["Таски"]
)

user = APIRouter(
#    prefix="/tasks",
    tags=["Юзеры"]
)



# Поддерживаемые методы
# @router.options("/items/{item_id}")
# async def get_items_options(current_user: Annotated[User, Depends(get_current_active_user)], item_id: int):
#     # Возвращаем информацию о поддерживаемых методах и заголовках для /items/{item_id}
#     return {"allowed_methods": ["GET", "POST", "PUT", "DELETE"]}


# Добавляем таску
@router.post("/tasks")
async def add_task(
        current_user: Annotated[User, Depends(get_current_active_user)], task: Annotated[STaskAdd, Depends()]
) -> STaskID:
    task_id = await TaskRepository.add_one(task)
    return {'ok': True, 'task_id': task_id}


# Смотрим все таски
@router.get("/tasks")
async def get_tasks(current_user: Annotated[User, Depends(get_current_active_user)]) -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks


# Смотрим конкретную таску по №
@router.get("/tasks/{task_№}")
async def get_task(current_user: Annotated[User, Depends(get_current_active_user)], task_nom: int):
    task, err = await TaskRepository.find_one(task_nom)
    if err == True:
        return task
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена") # вызываем ошибку


# Смотрим конкретную таску по id
@router.get("/tasks/{task_id}")
async def get_task(current_user: Annotated[User, Depends(get_current_active_user)], task_id: int):
    task, err = await TaskRepository.find_one_id(task_id)
    if err == True:
        return task
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена") # вызываем ошибку


#Удаляем конкретную таску по №
@router.delete("/tasks/{task_№}")
async def delete_task(current_user: Annotated[User, Depends(get_current_active_user)], task_nom: int):
    err = await TaskRepository.dell_one(task_nom)
    if err == True:
        return {"Таска уничтожена по порядковому номеру"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена") # вызываем ошибку


#Удаляем конкретную таску по id
@router.delete("/tasks/{task_id}")
async def delete_task(current_user: Annotated[User, Depends(get_current_active_user)], task_id: int):
    err = await TaskRepository.dell_one_id(task_id)
    if err == True:
        return {"Таска уничтожена по id"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена") # вызываем ошибку


# Заменяет существующую таску по №
@router.put("/tasks/{task_№}")
async def update_task(current_user: Annotated[User, Depends(get_current_active_user)], task: Annotated[STaskAdd, Depends()], task_nom: int):
    task_, err = await TaskRepository.update_one(task, task_nom)
    if err == 0:
        return {"Таска успешно заменена по порядковому номеру"}, task_
    elif err == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена")  # вызываем ошибку
    else:  # err == 2
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Перезапись не удалась")  # вызываем ошибку


# Заменяет существующую таску по id
@router.put("/tasks/{task_id}")
async def update_task(current_user: Annotated[User, Depends(get_current_active_user)], task: Annotated[STaskAdd, Depends()], task_id: int):
    task_, err = await TaskRepository.update_one_id(task, task_id)
    if err == 0:
        return {"Таска успешно заменена по id"}, task_
    elif err == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена") # вызываем ошибку
    else: # err == 2
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Перезапись не удалась") # вызываем ошибку


# Очистить таблицу
@router.delete("/tasks")
async def delete_all(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    await delete_tables()   # сначала дропаются все старые таблицы
    print("База очищена")
    await create_tables()   # асинхронное взаимодействие с базой
    print("База готова к работе")
    return {'Все таски уничтожены'}


###############################################################################################


# Тест домой
@router.get("/home")
async def get_home(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {'Чё каво??'}


# Стартовая страница
@router.get('/', response_class=HTMLResponse, include_in_schema=False) # include_in_schema=False - не отображать запрос на /docs
async def index():
    return FileResponse("index.html")

@router.get('/index.html', response_class=HTMLResponse) # include_in_schema=False - не отображать запрос на /docs
async def index():
    return FileResponse("index.html")


@router.get('/favicon.ico') # include_in_schema=False - не отображать запрос на /docs
async def favicon():
    return FileResponse("favicon.ico", media_type="image/x-icon") # "image/x-icon" или "image/vnd.microsoft.icon"?


@router.get('/Santex_download_1', include_in_schema=False) # include_in_schema=False - не отображать запрос на /docs
async def Santex():
    return FileResponse("Santex.mp4",
                        media_type="video/mp4",
                        filename="Чем уплотнять сантехническую резьбу лён, лента фум, нить, анаэробный герметик.mp4")

@router.get('/Santex_download_2', include_in_schema=False)
def Santex():
    def iterfile():
        with open("Santex.mp4", mode="rb") as file_like:
            yield from file_like
    return StreamingResponse(iterfile(), media_type="video/mp4")

# Модуль os.path предоставляет функции вроде exists(), isfile() и isdir(),
# которые позволяют проверить, существует ли путь, является ли он файлом или директорией соответственно.

async def php_html(file_path: str):
    if os.path.exists(file_path) and os.path.isfile(file_path):   # существует ли директория and является ли он файлом
        return FileResponse(path=file_path, media_type="html")
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.get('/delphibasics/{file_path:path}', response_class=HTMLResponse)
async def delphibasics_html(file_path: str):
    return await php_html("delphibasics/" + file_path)

@router.get('/electronics/{file_path:path}', response_class=HTMLResponse)
async def electronics_html(file_path: str):
    return await php_html("electronics/" + file_path)

# @router.get('/delphibasics/{item_id}', include_in_schema=False)
# async def php_html(item_id: str):
#     path_ = "delphibasics/" + item_id
#     return FileResponse(path=path_, media_type="html")
# # media_type="multipart/form-data" - скачать файл по ссылке
# # media_type="application/octet-stream" - скачать файл по ссылке
# # filename="mainpage.html" - можно обозвать файл иначе
#
# @router.get('/delphibasics/{item_id1}/{item_id2}', include_in_schema=False)
# async def php_html(item_id1: str, item_id2: str):
#     path_ = "delphibasics/" + item_id1 + "/" + item_id2
#     return FileResponse(path=path_, media_type="html")


###############################################################################################


@user.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@user.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "foo", "owner": current_user.username}]