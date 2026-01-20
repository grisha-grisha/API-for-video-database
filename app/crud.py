from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import models
import schemas


def create_video(db: Session, video: schemas.VideoCreate):
    """Создать новое видео в БД"""
    db_video = models.Video(
        video_path=video.video_path,
        start_time=video.start_time,
        duration=video.duration,
        camera_number=video.camera_number,
        location=video.location
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_video(db: Session, video_id: int):
    """Получить видео по ID"""
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def get_videos(
    db: Session,
    filters: Optional[schemas.VideoFilter] = None):
    """Получить список видео с фильтрацией"""
    query = db.query(models.Video)
    
    if filters:
        if filters.status:
            query = query.filter(models.Video.status.in_(filters.status))
        
        if filters.camera_number:
            query = query.filter(models.Video.camera_number.in_(filters.camera_number))
        
        if filters.location:
            query = query.filter(models.Video.location.in_(filters.location))

        if filters.start_time_from:
            query = query.filter(models.Video.start_time >= filters.start_time_from)
        
        if filters.start_time_to:
            query = query.filter(models.Video.start_time <= filters.start_time_to)
    
    return query.order_by(models.Video.created_at.desc()).all()


def update_video_status(
    db: Session, 
    video_id: int, 
    status: schemas.VideoStatus):
    """Обновить статус видео"""
    db_video = get_video(db, video_id)
    if db_video:
        db_video.status = status
        db.commit()
        db.refresh(db_video)
    return db_video


def delete_video(db: Session, video_id: int):
    """Удалить видео"""
    db_video = get_video(db, video_id)
    if db_video:
        db.delete(db_video)
        db.commit()
    return db_video