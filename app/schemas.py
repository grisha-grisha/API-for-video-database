from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional


class VideoCreate(BaseModel):
    """
    Схема для создания нового видео.
    Используется в POST /videos
    """
    video_path: str           # Путь к видео (обязательно)
    start_time: datetime      # Время начала (обязательно)
    duration: timedelta       # Длительность (обязательно)
    camera_number: int        # Номер камеры (обязательно)
    location: str             # Местоположение (обязательно)
    
    # Можно добавить простые проверки:
    class Config:
        # Минимальный пример проверок через аннотации
        # Более сложную валидацию добавим позже
        pass


class VideoUpdateStatus(BaseModel):
    """
    Схема для обновления статуса видео.
    Используется в PATCH /videos/{id}/status
    """
    status: str  # Новый статус


class VideoResponse(BaseModel):
    """
    Схема для ответа API при получении видео.
    Используется во всех GET запросах.
    """
    id: int                  # ID из базы данных
    video_path: str          # Путь к видео
    start_time: datetime     # Время начала
    duration: timedelta      # Длительность
    camera_number: int       # Номер камеры
    location: str            # Местоположение
    status: str              # Текущий статус
    created_at: datetime     # Время создания записи

    class Config:
        """
        Настройки Pydantic.
        from_attributes позволяет создавать схему из SQLAlchemy модели
        """
        from_attributes = True
