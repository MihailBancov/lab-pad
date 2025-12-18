from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.payment import PayRequest, PayResponse
from app.services.payments import process_payment


router = APIRouter(prefix="/payment", tags=["payment"])


@router.post("/pay", response_model=PayResponse)
def pay(payload: PayRequest, db: Session = Depends(get_db)):
    payment = process_payment(db, order_id=payload.order_id, amount_cents=payload.amount_cents)
    return PayResponse(ok=payment.status == "ok", status=payment.status)
