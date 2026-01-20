import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def init_db():
    """
    Создает все таблицы в базе данных.
    Вызывается при запуске приложения.
    """
    import models
    
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы в базе данных созданы/проверены")


def get_db():
    """
    Зависимость для получения сессии базы данных.
    Используется в эндпоинтах FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()