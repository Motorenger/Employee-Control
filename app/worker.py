import os
import time

from celery import Celery

from utils.system_config import envs


celery = Celery(__name__)
celery.conf.broker_url = envs.get("REDIS_URL")
celery.conf.result_backend = envs.get("REDIS_URL")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
