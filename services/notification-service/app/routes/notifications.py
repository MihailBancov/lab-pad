from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.notification import Notification
from app.schemas.notification import NotificationOut


router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_db() -> Session:
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[NotificationOut])
def list_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).order_by(Notification.id.desc()).limit(50).all()
