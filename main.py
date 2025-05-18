from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables

from router import router as tasks_router


@asynccontextmanager        # декоратор, позволяет создавать контекстные менеджеры
async def lifespan(app: FastAPI):
    await delete_tables()   # сначала дропаются все старые таблицы
    print("База очищена")
    await create_tables()   # асинхронное взаимодействие с базой
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)






