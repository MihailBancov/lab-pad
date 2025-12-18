from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product


def create_category(db: Session, *, name: str) -> Category:
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def create_product(
    db: Session,
    *,
    sku: str,
    name: str,
    description: str | None,
    price_cents: int,
    category_id: int | None,
) -> Product:
    product = Product(
        sku=sku,
        name=name,
        description=description,
        price_cents=price_cents,
        category_id=category_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
