from sqlalchemy import select
from database import new_session, TaskOrm
from schemas import STaskAdd, STask


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
    async def dell_one(cls, task_id: int) -> bool:
        async with new_session() as session:
            session.delete(task_id)

            return


    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [ STask.model_validate(task_model) for task_model in task_models ]
            return task_schemas


    @classmethod
    async def find_one(cls, task_id: int) -> (STask, bool):
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [ STask.model_validate(task_model) for task_model in task_models ]

            if (len(task_schemas) >= task_id and len(task_schemas) != 0 and task_id > 0):
                task = task_schemas[task_id-1]
                return task, True
            else:
                task = STask(name="", description="", id=0)
                return task, False