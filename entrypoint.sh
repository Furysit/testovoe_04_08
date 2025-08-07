#!/bin/sh

# Ждём базу
echo "⏳ Waiting for PostgreSQL"
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL is up"

# Применяем миграции
echo "Running alembic migrations"
alembic upgrade head


echo "Starting FastAPI"
uvicorn main:app --host 0.0.0.0 --port 8000
