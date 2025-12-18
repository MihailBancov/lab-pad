from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price_cents: int
    category_id: int | None = None


class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    description: str | None
    price_cents: int
    category_id: int | None

    class Config:
        from_attributes = True
