from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from db import crud, schemas
from core.security import get_current_user

router = APIRouter()

# Create a new product
@router.post("/create", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate):
    try:
        return crud.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Get all products
@router.get("/all", response_model=List[schemas.Product])
def get_products(
    current_user: schemas.User = Depends(get_current_user),
    category: Optional[str] = Query(None, min_length=1, max_length=50),
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
):
    try:
        products = crud.get_products(category, min_price, max_price)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
    return products

# Get a product by key
@router.get("/{key}", response_model=schemas.Product)
def get_product(key: str):
    try:
        product = crud.get_product(key)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# Update a product by key
@router.put("/update/{key}", response_model=schemas.Product)
def update_product(key: str, product: schemas.ProductUpdate):
    try:
        product = crud.update_product(key, product)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# Delete a product by key
@router.delete("/delete/{key}", response_model=schemas.Product)
def delete_product(key: str):
    try:
        product = crud.delete_product(key)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


