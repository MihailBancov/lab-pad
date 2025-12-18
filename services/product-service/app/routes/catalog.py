from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import require_admin
from app.db.session import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.catalog import CategoryCreate, CategoryOut, ProductCreate, ProductOut
from app.services.catalog import create_category, create_product


router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.post("/categories", response_model=CategoryOut, dependencies=[Depends(require_admin)])
def add_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(db, name=payload.name)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category already exists")


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()


@router.post("/products", response_model=ProductOut, dependencies=[Depends(require_admin)])
def add_product(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_product(
            db,
            sku=payload.sku,
            name=payload.name,
            description=payload.description,
            price_cents=payload.price_cents,
            category_id=payload.category_id,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="SKU already exists")


@router.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id).all()


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
