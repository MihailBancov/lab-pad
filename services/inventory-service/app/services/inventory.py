from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_item import InventoryItem


def set_quantity(db: Session, *, product_id: int, quantity: int) -> InventoryItem:
    item = db.get(InventoryItem, product_id)
    if not item:
        item = InventoryItem(product_id=product_id, quantity=quantity)
        db.add(item)
    else:
        item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def reserve(db: Session, *, items: list[tuple[int, int]]) -> tuple[bool, str | None]:
    # lock rows to avoid concurrent oversell
    for product_id, qty in items:
        row = db.execute(
            select(InventoryItem).where(InventoryItem.product_id == product_id).with_for_update()
        ).scalar_one_or_none()
        available = row.quantity if row else 0
        if available < qty:
            db.rollback()
            return False, f"Not enough stock for product_id={product_id}"

    for product_id, qty in items:
        row = db.get(InventoryItem, product_id)
        if not row:
            row = InventoryItem(product_id=product_id, quantity=0)
            db.add(row)
            db.flush()
        row.quantity -= qty

    db.commit()
    return True, None
