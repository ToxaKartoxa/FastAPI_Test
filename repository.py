from sqlalchemy import select

from database import new_session, TaskOrm
from schemas import STaskAdd, STask


#from main import STaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()      # await ожидание конца синхронной операции
            return task.id


    @classmethod
    async def find_one(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [ STask.model_validate(task_model) for task_model in task_models ]
            return task_schemas