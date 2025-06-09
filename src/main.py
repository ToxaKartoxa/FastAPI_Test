from fastapi import FastAPI
from contextlib import asynccontextmanager

from . database import create_tables, delete_tables
from . router import router as tasks_router, user as user_router

from fastapi.middleware.cors import CORSMiddleware

####################################################################################

@asynccontextmanager        # декоратор, позволяет создавать контекстные менеджеры
async def lifespan(app: FastAPI):
    # await delete_tables()   # сначала дропаются все старые таблицы
    # print("База очищена")
    await create_tables()   # асинхронное взаимодействие с базой
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(user_router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены, например: ["https://example.com"]
    allow_credentials=True,
#    allow_methods=["HEAD", "PATCH", "TRACE"],
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"],  # Разрешить все методы, включая OPTIONS
    allow_headers=["*"],  # Разрешить все заголовки
)

####################################################################################

