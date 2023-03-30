import os, sys
import importlib

from celery import Celery
from celery.schedules import crontab


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("REDIS_URL")
celery.conf.result_backend = os.environ.get("REDIS_URL")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        notifications.s(),
        name='notifications'
    )


@celery.task()
async def notifications():
        get_db = importlib.import_module('db.database.get_db')
        QuizzService = importlib.import_module('services.quizz_logic.QuizzService')
        quizz_service = QuizzService(db=get_db())
        await quizz_service.check_passing()
