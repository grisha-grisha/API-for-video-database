from sqlalchemy import Column, Integer, String, DateTime, Interval, Enum
from sqlalchemy.sql import func
import enum
from database import Base


class VideoStatusEnum(str, enum.Enum):
    """Enum для статусов видео в БД"""
    NEW = "new"
    TRANSCODED = "transcoded"
    RECOGNIZED = "recognized"


class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Interval, nullable=False)
    camera_number = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    status = Column(
        Enum(VideoStatusEnum, name="video_status"),
        default=VideoStatusEnum.NEW,
        nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())