from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

import database
import models
import crud
import schemas
from database import get_db

app = FastAPI(
    title="Video API",
    description="API для управления видео записями",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    """Создаем таблицы при запуске"""
    models.Base.metadata.create_all(bind=database.engine)
    print("База данных готова!")


@app.post("/videos", 
          response_model=schemas.VideoResponse, 
          status_code=status.HTTP_201_CREATED,
          summary="Добавить новое видео",
          description="Добавляет новое видео в базу данных. Статус автоматически устанавливается в 'new'.")
def create_video(
    video: schemas.VideoCreate,
    db: Session = Depends(get_db)
):
    """Добавить новое видео в БД"""
    return crud.create_video(db=db, video=video)


@app.get("/videos",
         response_model=List[schemas.VideoResponse],
         summary="Получить список видео",
         description="Возвращает список всех видео с поддержкой фильтров.")
def read_videos(
    status: Optional[List[schemas.VideoStatus]] = Query(
        None, 
        description="Фильтр по статусам (можно указать несколько)"
    ),
    camera_number: Optional[List[int]] = Query(
        None, 
        description="Фильтр по номерам камер (можно указать несколько)"
    ),
    location: Optional[List[str]] = Query(
        None, 
        description="Фильтр по локациям (можно указать несколько)"
    ),
    start_time_from: Optional[datetime] = Query(
        None, 
        description="Видео после указанного времени"
    ),
    start_time_to: Optional[datetime] = Query(
        None, 
        description="Видео до указанного времени"
    ),
    db: Session = Depends(get_db)
):
    """Получить список всех видео с фильтрами"""
    filters = schemas.VideoFilter(
        status=status,
        camera_number=camera_number,
        location=location,
        start_time_from=start_time_from,
        start_time_to=start_time_to
    )
    videos = crud.get_videos(db, filters=filters)
    return videos


@app.get("/videos/{video_id}",
         response_model=schemas.VideoResponse,
         summary="Получить видео по ID",
         description="Возвращает детальную информацию о видео по его ID.")
def read_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Получить информацию о конкретном видео по ID"""
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Видео с ID {video_id} не найдено"
        )
    return db_video


@app.patch("/videos/{video_id}/status",
           response_model=schemas.VideoResponse,
           summary="Обновить статус видео",
           description="Обновляет статус видео. Допустимые значения: 'new', 'transcoded', 'recognized'.")
def update_video_status(
    video_id: int,
    status_update: schemas.VideoUpdateStatus,
    db: Session = Depends(get_db)
):
    """Обновить статус видео"""
    db_video = crud.update_video_status(db, video_id, status_update.status)
    if db_video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Видео с ID {video_id} не найдено"
        )
    return db_video