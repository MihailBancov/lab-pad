from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.db.migrations import apply_migrations
from app.pages.home import render_home
from app.routes.auth import router as auth_router


def create_app() -> FastAPI:
    apply_migrations()
    app = FastAPI(title=settings.service_name)
    app.include_router(auth_router)

    @app.get("/")
    def root():
        return HTMLResponse(content=render_home())

    @app.get("/health")
    def health():
        return {"status": "ok", "service": settings.service_name}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=False)
