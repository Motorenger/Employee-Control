from datetime import datetime

from fastapi.middleware import Middleware

from sqlalchemy.ext.asyncio import create_async_engine
from starlette.types import ASGIApp, Receive, Scope, Send

from apscheduler.datastores.async_sqlalchemy import AsyncSQLAlchemyDataStore
from apscheduler.eventbrokers.asyncpg import AsyncpgEventBroker
from apscheduler.schedulers.async_ import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

from db.database import get_db
from utils.system_config import envs
from services.quizz_logic import QuizzService


async def notifications():
    db = get_db()
    await db.connect()
    quizz_service = QuizzService(db=get_db())
    await quizz_service.check_passing()


class SchedulerMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        scheduler: AsyncScheduler,
    ) -> None:
        self.app = app
        self.scheduler = scheduler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            async with self.scheduler:
                await self.scheduler.add_schedule(
                    notifications, IntervalTrigger(hours=24), id="notifications"
                )
                await self.scheduler.start_in_background()
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)


engine = create_async_engine(envs.get("DATABASE_URL"))
data_store = AsyncSQLAlchemyDataStore(engine)
event_broker = AsyncpgEventBroker.from_async_sqla_engine(engine)
scheduler = AsyncScheduler()
middleware = [Middleware(SchedulerMiddleware, scheduler=scheduler)]
