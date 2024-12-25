from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import User
from repository import user_crud
from schemas import user_schema
from security.user_security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    verify_token,
)

router = APIRouter(prefix="/user", tags=["User"])


# create user
@router.post("/create", response_model=user_schema.RegisterResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    user_crud.create_user(db=db, user=user)
    return {"message": "User created successfully"}


# login user
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(User=user)
    return {"access_token": access_token, "token_type": "bearer"}


# update role:
@router.put("/update/{user_id}/role", response_model=user_schema.User)
def update_user_role(
    user_id: int,
    new_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.roles != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can update roles.",
        )
    if new_role not in ["user", "admin", "guest"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role."
        )

    user = user_crud.update_user_role(db=db, user_id=user_id, new_role=new_role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user


@router.delete("/users/{user_id}", response_model=user_schema.RegisterResponse)
async def delete_user(user_id: int, role: str):
    user_delete = user_crud.UserDelete()
    result = user_delete.delete_user(user_id, role)

    if "Permission denied" in result["message"]:
        raise HTTPException(status_code=403, detail=result["message"])

    return result
