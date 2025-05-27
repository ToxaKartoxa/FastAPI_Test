from sqlalchemy import select
from database import new_session, TaskOrm
from schemas import STaskAdd, STask


class TaskRepository:

    # Добавляем таску
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()       # синхронизируем изменения, внесенные в сессию
            await session.commit()      # завершаем транзакцию и делаем изменения постоянными в базе данных
            # await ожидание конца синхронной операции
            return task.id


    # Удаляем конкретную таску по №
    @classmethod
    async def dell_one(cls, task_nom: int) -> bool:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            if (len(task_models) >= task_nom and len(task_models) != 0 and task_nom > 0):
                await session.delete(task_models[task_nom-1])
                await session.commit()
                return True
            else:
                return False


    # Удаляем конкретную таску по id
    @classmethod
    async def dell_one_id(cls, task_id: int) -> bool:
        async with new_session() as session:
            # Получаем таску
            user = await session.get(TaskOrm, task_id)
            if not user:
                return False
            else:
                await session.delete(user)
                await session.commit()
                return True


    # Заменяет существующую таску по №
    @classmethod
    async def update_one(cls, data: STaskAdd, task_nom: int) -> (STask, bool):
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            if (len(task_models) >= task_nom and len(task_models) != 0 and task_nom > 0):
                # task_dict = data.model_dump()
                # await session.refresh(task_models[task_nom-1], task_dict)
                task = STask.model_validate(task_models[task_nom - 1])
                task_, err = await TaskRepository.update_one_id(data, task.id)
                return task_, err
            else:
                task = STask(name="", description="", id=0)
                return task, False


    # Заменяет существующую таску по id
    @classmethod
    async def update_one_id(cls, data: STaskAdd, task_id: int) -> (STask, int):
        async with new_session() as session:
            # Получаем таску
            user = await session.get(TaskOrm, task_id)
            if not user:
                task = STask(name="", description="", id=0)
                return task, 1 # - таска не найдена
            else:
                # Обновляем таску
                user.name = data.name
                user.description = data.description
                user.id = task_id
                await session.commit()
                # Обновляем объект в сессии
                await session.refresh(user)
                # Проверяем, что таска обновлена
                user = await session.get(TaskOrm, task_id)
                task = STask.model_validate(user)
                task_set = STask(name=data.name, description=data.description, id=task_id)
                if task_set == task:
                    return task, 0 # - ok
                else:
                    return task, 2 # - Перезапись не удалась


    # Смотрим все таски
    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [ STask.model_validate(task_model) for task_model in task_models ]
            return task_schemas


    # Смотрим конкретную таску по №
    @classmethod
    async def find_one(cls, task_nom: int) -> (STask, bool):
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            if (len(task_models) >= task_nom and len(task_models) != 0 and task_nom > 0):
                task = STask.model_validate(task_models[task_nom-1])
                return task, True
            else:
                task = STask(name="", description="", id=0)
                return task, False


    # Смотрим конкретную таску по id
    @classmethod
    async def find_one_id(cls, task_id: int) -> (STask, bool):
        async with new_session() as session:
            user = await session.get(TaskOrm, task_id)
            if not user:
                task = STask(name="", description="", id=0)
                return task, False
            else:
                task = STask.model_validate(user)
                return task, True