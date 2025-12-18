from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_cents: int


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_cents: int
    items: list[OrderItemOut]
