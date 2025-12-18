from __future__ import annotations

import httpx

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.order import CreateOrderRequest, OrderOut, OrderItemOut
from app.services.kafka import kafka_publisher
from app.services.order_flow import create_order_end_to_end
from app.core.config import settings


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut)
async def create_order(
    payload: CreateOrderRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    authorization: str | None = Header(default=None),
):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    user_id = int(user["sub"])
    items = [(i.product_id, i.quantity) for i in payload.items]
    if not items:
        raise HTTPException(status_code=400, detail="Empty items")

    try:
        order, order_items = await create_order_end_to_end(
            db, user_id=user_id, items=items, bearer_token=authorization
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    # Publish event for notification service
    await kafka_publisher.publish(
        settings.kafka_order_events_topic,
        {
            "type": "order.status_changed",
            "order_id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_cents": order.total_cents,
        },
    )

    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total_cents=order.total_cents,
        items=[
            OrderItemOut(product_id=oi.product_id, quantity=oi.quantity, price_cents=oi.price_cents)
            for oi in order_items
        ],
    )
