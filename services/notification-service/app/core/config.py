from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "notification-service"
    port: int = 8006
    database_url: str
    jwt_secret: str
    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_order_events_topic: str = "order-events"
    kafka_consumer_group: str = "notification-service"


settings = Settings()
