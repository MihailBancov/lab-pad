from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "order-service"
    port: int = 8004
    database_url: str
    jwt_secret: str
    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_order_events_topic: str = "order-events"
    product_service_url: str
    inventory_service_url: str
    payment_service_url: str


settings = Settings()
