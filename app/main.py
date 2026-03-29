# app/main.py
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


# 1. POST /videos - создание видео
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


# 2. GET /videos - получение видео с фильтрами
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


# 3. GET /videos/statuses - получить список всех возможных статусов
@app.get("/videos/statuses",
         summary="Получить список статусов",
         description="Возвращает список всех возможных статусов видео.")
def get_statuses():
    """Получить все возможные статусы"""
    return {"statuses": ["new", "transcoded", "recognized"]}


# 4. GET /videos/cameras - получить список всех камер
@app.get("/videos/cameras",
         summary="Получить список камер",
         description="Возвращает список всех номеров камер, которые есть в БД.")
def get_cameras(db: Session = Depends(get_db)):
    """Получить все номера камер"""
    cameras = db.query(models.Video.camera_number).distinct().all()
    return {"cameras": [c[0] for c in cameras]}


# 5. GET /videos/locations - получить список всех локаций
@app.get("/videos/locations",
         summary="Получить список локаций",
         description="Возвращает список всех локаций, которые есть в БД.")
def get_locations(db: Session = Depends(get_db)):
    """Получить все локации"""
    locations = db.query(models.Video.location).distinct().all()
    return {"locations": [l[0] for l in locations]}


# 6. GET /health - проверка здоровья
@app.get("/health",
         summary="Проверка здоровья",
         description="Проверяет работоспособность API и подключение к БД.")
def health_check(db: Session = Depends(get_db)):
    """Проверка здоровья приложения"""
    try:
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# 7. DELETE /videos/{video_id} - удалить видео
@app.delete("/videos/{video_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Удалить видео",
            description="Удаляет видео по ID.")
def delete_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Удалить видео"""
    db_video = crud.delete_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Видео с ID {video_id} не найдено"
        )
    return None


# 8. PATCH /videos/{video_id}/location - обновить локацию видео
@app.patch("/videos/{video_id}/location",
           response_model=schemas.VideoResponse,
           summary="Обновить локацию видео",
           description="Обновляет локацию видео.")
def update_video_location(
    video_id: int,
    location: str = Query(..., min_length=1, description="Новая локация"),
    db: Session = Depends(get_db)
):
    """Обновить локацию видео"""
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Видео с ID {video_id} не найдено"
        )
    db_video.location = location
    db.commit()
    db.refresh(db_video)
    return db_video


# 9. GET /videos/{video_id} - получение видео по ID (ДОЛЖЕН БЫТЬ ПОСЛЕДНИМ)
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


# 10. PATCH /videos/{video_id}/status - обновление статуса
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