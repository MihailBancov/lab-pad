import json
from typing import Any

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class KafkaPublisher:
    def __init__(self) -> None:
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def publish(self, topic: str, event: dict[str, Any]) -> None:
        if not self._producer:
            raise RuntimeError("Kafka producer not started")
        payload = json.dumps(event).encode("utf-8")
        await self._producer.send_and_wait(topic, payload)


kafka_publisher = KafkaPublisher()
