from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "inventory-service"
    port: int = 8003
    database_url: str
    jwt_secret: str
    kafka_bootstrap_servers: str = "kafka:9092"


settings = Settings()
