from __future__ import annotations

import asyncio
import json

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.db.session import get_db_session
from app.models.notification import Notification


class OrderEventsConsumer:
    def __init__(self) -> None:
        self._consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task[None] | None = None
        self._runner: asyncio.Task[None] | None = None

    async def start(self) -> None:
        self._consumer = AIOKafkaConsumer(
            settings.kafka_order_events_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=settings.kafka_consumer_group,
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        await self._consumer.start()
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            self._task = None
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None

    async def run_forever(self) -> None:
        backoff_seconds = 1
        while True:
            try:
                await self.start()
                backoff_seconds = 1
                assert self._task is not None
                await self._task
            except asyncio.CancelledError:
                await self.stop()
                raise
            except Exception:
                await self.stop()
                await asyncio.sleep(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, 30)

    async def _run(self) -> None:
        assert self._consumer is not None
        async for msg in self._consumer:
            try:
                event = json.loads(msg.value.decode("utf-8"))
            except Exception:
                continue

            if event.get("type") != "order.status_changed":
                continue

            user_id = int(event.get("user_id"))
            order_id = int(event.get("order_id"))
            status = str(event.get("status"))

            db = get_db_session()
            try:
                n = Notification(
                    user_id=user_id,
                    order_id=order_id,
                    channel="email",
                    message=f"Order #{order_id} status changed to {status}",
                    status="sent",
                )
                db.add(n)
                db.commit()
            finally:
                db.close()


order_events_consumer = OrderEventsConsumer()
