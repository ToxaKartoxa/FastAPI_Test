# подключаем асинхронно бд
# библиотека sqlalchemy суперпоаулярная билиотека для работы с реализационными бд на пу

# импорт асинхронного движка для работы с бд

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# сосздаем асинх движок, который будет отпралять запросы в бд
engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
    # URL бд
    # sqlite - название бд
    # aiosqlite - драйвер
    # tasks.db - файл бд (может жить и на сервере по адресу)
)

# async_sessionmaker - фабрика для создания сессий, открытие транзакция для работы с бд
new_session = async_sessionmaker(engine, expire_on_commit=False)
# expire_on_commit - параметр разбирается в курсе по алхимии


class Model(DeclarativeBase):       # пустой класс типо для конфигураций
    pass                            # в курсах про алхимию все расписано


class TaskOrm(Model):               # описание таблицы
    __tablename__ = 'task'          # название
    id: Mapped[int] = mapped_column(primary_key=True)   # первичный ключ
    name: Mapped[str]
    description: Mapped[str | None]

async def create_tables():    # асинхронная функция для создание таблиц (потомучто ипозльзуем асинх. драйвер aiosqlite)
    async with engine.begin() as conn:      # которая обращается к engine, который отправляет запросы
        await conn.run_sync(Model.metadata.create_all)      # и создавать все таблицы

async def delete_tables():    # функция для удаления таблиц (тестовый проект, обычно не используется)
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)