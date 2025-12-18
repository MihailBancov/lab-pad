from __future__ import annotations

from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.order import Order
from app.models.order_item import OrderItem


def _sum_total(items: list[tuple[int, int, int]]) -> int:
    # items: (product_id, quantity, price_cents)
    return sum(qty * price for _, qty, price in items)


async def create_order_end_to_end(
    db: Session,
    *,
    user_id: int,
    items: list[tuple[int, int]],
    bearer_token: str,
) -> tuple[Order, list[OrderItem]]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1) Fetch product prices
        detailed: list[tuple[int, int, int]] = []
        for product_id, qty in items:
            r = await client.get(f"{settings.product_service_url}/catalog/products/{product_id}")
            r.raise_for_status()
            product: dict[str, Any] = r.json()
            detailed.append((product_id, qty, int(product["price_cents"])))

        # 2) Reserve inventory
        reserve_payload = {"items": [{"product_id": pid, "quantity": qty} for pid, qty in items]}
        r = await client.post(f"{settings.inventory_service_url}/inventory/reserve", json=reserve_payload)
        r.raise_for_status()
        reserve_res = r.json()
        if not reserve_res.get("ok"):
            raise RuntimeError(reserve_res.get("reason") or "reserve_failed")

        total_cents = _sum_total(detailed)

        # 3) Create order (status created)
        order = Order(user_id=user_id, status="created", total_cents=total_cents)
        db.add(order)
        db.commit()
        db.refresh(order)

        order_items: list[OrderItem] = []
        for product_id, qty, price_cents in detailed:
            oi = OrderItem(order_id=order.id, product_id=product_id, quantity=qty, price_cents=price_cents)
            db.add(oi)
            order_items.append(oi)
        db.commit()

        # 4) Call payment stub
        pay_payload = {"order_id": order.id, "amount_cents": total_cents}
        r = await client.post(f"{settings.payment_service_url}/payment/pay", json=pay_payload)
        r.raise_for_status()
        pay_res = r.json()

        if pay_res.get("ok"):
            order.status = "paid"
        else:
            order.status = "payment_failed"

        db.commit()
        db.refresh(order)
        return order, order_items
