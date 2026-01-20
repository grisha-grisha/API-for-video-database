from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum

class VideoStatus(str, Enum):
    """Статусы видео"""
    NEW = "new"
    TRANSCODED = "transcoded"
    RECOGNIZED = "recognized"


class VideoBase(BaseModel):
    """Базовая схема для видео"""
    video_path: str = Field(..., min_length=1, description="Путь до видеофайла")
    start_time: datetime = Field(..., description="Время начала записи")
    duration: timedelta = Field(..., description="Длительность видео")
    camera_number: int = Field(..., gt=0, description="Номер камеры")
    location: str = Field(..., min_length=1, description="Локация")
    
    @validator('video_path')
    def video_path_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('video_path не должен быть пустым')
        return v.strip()
    
    @validator('duration')
    def duration_positive(cls, v):
        if v <= timedelta(0):
            raise ValueError('duration должен быть положительным')
        return v
    
    @validator('camera_number')
    def camera_number_positive(cls, v):
        if v <= 0:
            raise ValueError('camera_number должен быть положительным')
        return v
    
    @validator('location')
    def location_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('location не должна быть пустой')
        return v.strip()


class VideoCreate(VideoBase):
    """Схема для создания видео (POST)"""
    pass


class VideoUpdateStatus(BaseModel):
    """Схема для обновления статуса (PATCH)"""
    status: VideoStatus = Field(..., description="Новый статус")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["new", "transcoded", "recognized"]
        if v not in valid_statuses:
            raise ValueError(f'status должен быть одним из: {valid_statuses}')
        return v


class VideoResponse(VideoBase):
    """Схема для ответа API"""
    id: int
    status: VideoStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, json_encoders={
        timedelta: lambda td: str(td)  # Конвертируем timedelta в строку
    })


class VideoFilter(BaseModel):
    """Схема для фильтрации видео (GET)"""
    status: Optional[List[VideoStatus]] = None
    camera_number: Optional[List[int]] = None
    location: Optional[List[str]] = None
    start_time_from: Optional[datetime] = None
    start_time_to: Optional[datetime] = None
