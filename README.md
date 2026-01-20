# Video API Service

REST API для управления видео записями с использованием FastAPI и PostgreSQL.

### Предварительные требования
- Docker
- Docker Compose

### Запуск в Docker

1. **Клонируйте репозиторий и перейдите в директорию проекта:**
```bash
cd API-for-video-database

2. **При необходимости отредактируйте .env файл (опционально):**

3. **Запустите приложение:**
docker-compose up --build -d

4. **Проверьте статус:**
docker-compose ps

5. **API будет доступно по адресу:**
- Приложение: http://localhost:8000
- Документация Swagger: http://localhost:8000/docs

5. **Остановка:**
docker-compose down
