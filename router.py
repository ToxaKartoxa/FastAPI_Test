from typing import Annotated, Any, Coroutine

from OAuth2 import authenticate_user, fake_users_db, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token
from repository import TaskRepository
from schemas import STaskAdd, STask, STaskID, Token, User

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends, HTTPException, status, APIRouter
from datetime import timedelta



router = APIRouter(
#    prefix="/tasks",
    tags=["Таски"]
)

user = APIRouter(
#    prefix="/tasks",
    tags=["Юзеры"]
)


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


# Смотрим конкретную таску по id
@router.get("/tasks/{task_id}")
async def get_task(current_user: Annotated[User, Depends(get_current_active_user)], task_id: int) -> STask:
    task, err = await TaskRepository.find_one(task_id)
    if err == True:
        return task
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Таска не найдена") # вызываем ошибку


# Тест домой
@router.get("/home")
async def get_home(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {'Чё каво??'}


####################################################################################


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
    return [{"item_id": "нипонятно", "owner": current_user.username}]