from pydantic import BaseModel


class PayRequest(BaseModel):
    order_id: int
    amount_cents: int


class PayResponse(BaseModel):
    ok: bool
    status: str
