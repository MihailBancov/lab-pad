from pydantic import BaseModel


class SetQuantityRequest(BaseModel):
    product_id: int
    quantity: int


class InventoryOut(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class ReserveItem(BaseModel):
    product_id: int
    quantity: int


class ReserveRequest(BaseModel):
    items: list[ReserveItem]


class ReserveResponse(BaseModel):
    ok: bool
    reason: str | None = None
