from sqlalchemy import Column, Integer, String, DateTime, Interval
from sqlalchemy.sql import func
from .database import Base


class Video(Base):
    __tablename__ = "videos"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    video_path = Column(
        String,
        nullable=False
    )
    start_time = Column(
        DateTime,
        nullable=False
    )
    duration = Column(
        Interval,
        nullable=False
    )
    camera_number = Column(
        Integer,
        nullable=False
    )
    location = Column(
        String,
        nullable=False
    )
    status = Column(
        String,
        default="new",
        nullable=False
    )
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
