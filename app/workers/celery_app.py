from celery import Celery

from app.core.config import settings

celery_app = Celery(
    settings.app_name,
    broker=settings.redis.url,
    include=["app.workers.tasks"],
)
