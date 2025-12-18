from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_admin
from app.db.session import get_db
from app.models.inventory_item import InventoryItem
from app.schemas.inventory import InventoryOut, ReserveRequest, ReserveResponse, SetQuantityRequest
from app.services.inventory import reserve, set_quantity


router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/set", response_model=InventoryOut, dependencies=[Depends(require_admin)])
def api_set(payload: SetQuantityRequest, db: Session = Depends(get_db)):
    return set_quantity(db, product_id=payload.product_id, quantity=payload.quantity)


@router.get("/{product_id}", response_model=InventoryOut)
def api_get(product_id: int, db: Session = Depends(get_db)):
    item = db.get(InventoryItem, product_id)
    if not item:
        return InventoryOut(product_id=product_id, quantity=0)
    return item


@router.post("/reserve", response_model=ReserveResponse)
def api_reserve(payload: ReserveRequest, db: Session = Depends(get_db)):
    ok, reason = reserve(db, items=[(i.product_id, i.quantity) for i in payload.items])
    return ReserveResponse(ok=ok, reason=reason)
