import random

from sqlalchemy.orm import Session

from app.models.payment import Payment


def process_payment(db: Session, *, order_id: int, amount_cents: int, ok_probability: float = 0.9) -> Payment:
    ok = random.random() < ok_probability
    status = "ok" if ok else "failed"
    payment = Payment(order_id=order_id, amount_cents=amount_cents, status=status)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
