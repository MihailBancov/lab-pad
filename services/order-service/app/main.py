from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.db.migrations import apply_migrations
from app.pages.home import render_home
from app.routes.orders import router as orders_router
from app.services.kafka import kafka_publisher


def create_app() -> FastAPI:
    apply_migrations()
    app = FastAPI(title=settings.service_name)
    app.include_router(orders_router)

    @app.get("/")
    def root():
        return HTMLResponse(content=render_home())

    @app.on_event("startup")
    async def _startup() -> None:
        await kafka_publisher.start()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await kafka_publisher.stop()

    @app.get("/health")
    def health():
        return {"status": "ok", "service": settings.service_name}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=False)
