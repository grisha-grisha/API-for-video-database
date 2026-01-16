import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Получаем значения ИЗ ОДИНАКОВЫХ переменных что и в docker-compose
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# URL для подключения к PostgreSQL
# Формат: postgresql://user:password@host:port/database
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"

# Создаем "движок" для подключения к БД
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,  # Не коммитить автоматически
    autoflush=False,   # Не сбрасывать изменения автоматически
    bind=engine        # Привязываем к нашему движку
)

# Базовый класс для всех моделей
Base = declarative_base()


def init_db():
    """
    Создает все таблицы в базе данных.
    Вызывается при запуске приложения.
    """
    # Импортируем модели здесь, чтобы избежать циклических импортов
    from . import models
    
    # Создаем все таблицы, определенные в моделях
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы в базе данных созданы/проверены")


def get_db():
    """
    Зависимость для получения сессии базы данных.
    Используется в эндпоинтах FastAPI.
    """
    db = SessionLocal()
    try:
        yield db  # Отдаем сессию FastAPI
    finally:
        db.close()  # Закрываем сессию после использования