from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import OAuth2PasswordBearer
from models import user_model
from repository import product_crud
from schemas import product_schema
from security.user_security import authenticate_user, get_current_user, verify_token


router = APIRouter(prefix="/product")


# Create a product
@router.post(
    "/products/", response_model=product_schema.Product, tags=["product"]
)
async def create_product(
    name: str,
    description: str,
    price: float,
    new_price: float,
    files: List[UploadFile] = File(...),
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if the current user is an admin
    if current_user.roles != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    # Create product and save images
    created_product = product_crud.create_product(
        db=db,
        name=name,
        description=description,
        price=price,
        new_price=new_price,
        image_files=files,
    )

    return created_product


# Get all products
@router.get(
    "/products/", response_model=List[product_schema.Product], tags=["product"]
)
def read_products(db: Session = Depends(get_db)):
    products = product_crud.get_products(db=db)
    return products


# Get product by ID
@router.get(
    "/products/{product_id}", response_model=product_schema.Product, tags=["product"]
)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# update product if admin is the user:
@router.put(
    "/products/{product_id}", response_model=product_schema.Product, tags=["product"]
)
def update_product(
    product_id: int,
    name: str,
    description: str,
    price: float,
    new_price: float,
    files: List[UploadFile] = File(...),
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.roles != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    updated_product = product_crud.update_product(
        db=db,
        product_id=product_id,
        name=name,
        description=description,
        price=price,
        new_price=new_price,
        image_files=files,
    )

    return updated_product


# delete product if admin is the user:
@router.delete(
    "/products/{product_id}", response_model=product_schema.Product, tags=["product"]
)
def delete_product(
    product_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.roles != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    deleted_product = product_crud.delete_product(db=db, product_id=product_id)

    return deleted_product
