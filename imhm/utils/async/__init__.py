# -*- coding:utf-8 -*-
from datetime import timedelta
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

        "interrupt_timer": {
            "task": "imhm.utils.async.functions.interrupt_timer",
            "schedule": timedelta(seconds=60)
        },

        "warning_processor": {
            "task": "imhm.utils.async.functions.warning_processor",
            "schedule": timedelta(seconds=15)
        }
    }

celery_app = Celery(current_app, include=["functions"])
celery_app.config_from_object(Config)
