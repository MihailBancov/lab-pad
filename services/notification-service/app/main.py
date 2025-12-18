import asyncio

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.db.migrations import apply_migrations
from app.pages.home import render_home
from app.routes.notifications import router as notifications_router
from app.services.consumer import order_events_consumer


def create_app() -> FastAPI:
    apply_migrations()
    app = FastAPI(title=settings.service_name)
    app.include_router(notifications_router)

    @app.get("/")
    def root():
        return HTMLResponse(content=render_home())

    @app.on_event("startup")
    async def _startup() -> None:
        app.state.consumer_task = asyncio.create_task(order_events_consumer.run_forever())

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        task = getattr(app.state, "consumer_task", None)
        if task:
            task.cancel()
        await order_events_consumer.stop()

    @app.get("/health")
    def health():
        return {"status": "ok", "service": settings.service_name}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=False)
