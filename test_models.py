import sys
sys.path.append('.')
from datetime import datetime, timedelta
from app.database import engine, init_db
from app.models import Base

# 1. Создаем таблицы
print("Создаем таблицы в БД...")
init_db()
print("✅ Таблицы созданы!")

# 2. Проверяем структуру таблицы
from sqlalchemy import inspect
inspector = inspect(engine)
columns = inspector.get_columns('videos')
print("\nСтруктура таблицы 'videos':")
for column in columns:
    print(f"  - {column['name']}: {column['type']}")