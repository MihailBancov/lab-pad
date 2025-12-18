from __future__ import annotations

from pathlib import Path

from app.core.config import settings

_HOME_HTML: str | None = None


def render_home() -> str:
    global _HOME_HTML
    if _HOME_HTML is None:
        html_path = Path(__file__).with_name("home.html")
        _HOME_HTML = html_path.read_text(encoding="utf-8")
    return _HOME_HTML.replace("__SERVICE_NAME__", settings.service_name)
