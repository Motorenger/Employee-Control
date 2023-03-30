import asyncio
import os

from celery import Celery, shared_task


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("REDIS_URL")
celery.conf.result_backend = os.environ.get("REDIS_URL")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, notifications.s(), name='notifications')

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

@celery.task()
async def notifications():
    print(a)


celery.conf.beat_schedule = {
    'notifications': {
        'task': 'tasks.add',
        'schedule': 10.0,
    },
}
celery.conf.timezone = 'UTC'
