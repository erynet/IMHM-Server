# -*- coding:utf-8 -*-
from celery import Celery
from celery.schedules import crontab
from flask import current_app


# object
class Config:
    BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    CELERY_ENABLE_UTC = False
    CELERY_ACCEPT_CONTENT = ["pickle", "json", "msgpack", "yaml"]

    CELERYBEAT_SCHEDULE = {
        "expired_order": {
            "task": "functions.expired_order",
            "schedule": crontab(hour=3, minute=19)
        }
    }

celery_app = Celery(current_app, include=["functions"])
celery_app.config_from_object(Config)
