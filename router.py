from typing import Annotated
from fastapi import Depends, APIRouter
#from main import tasks
from repository import TaskRepository
from schemas import STaskAdd, STask, STaskID

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"]
)

@router.post("")
async def add_task(
        task: Annotated[STaskAdd, Depends()]
) -> STaskID:
    task_id = await TaskRepository.add_one(task)
    return {'ok': True, 'task_id': task_id}

@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_one() # find_all
    return tasks






# @app.get("/home")
# def get_home():
#     return {'Hello World'}