#!/bin/bash
# Start Celery worker in background
celery -A app.worker.tasks worker --loglevel=info --pool=solo &

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
