from typing import List
from models.user_model import User
from database.connection import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel, conint, constr
from schemas import user_schema
from fastapi import HTTPException, status, Depends
from security.user_security import hash_password


# get user by id:
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


# get user by username:
def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


# get user by email:
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


# get all users:
def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


# create user:
def create_user(db: Session, user: user_schema.UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        roles=user.roles,
        is_active=user.is_active,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# update user role:
def update_user_role(db: Session, user_id: int, new_role: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.roles = new_role
        db.commit()
        db.refresh(user)
        return user
    return None


class RoleUpdateRequest(BaseModel):
    new_role: constr(strip_whitespace=True, min_length=3, max_length=20)  # type: ignore


# delete user:
class UserDelete(BaseModel):
    user_id: int

    def delete_user(self, user_id: int, role: str):
        if role == "admin":
            # Logic to delete the user
            return {"message": f"User {user_id} deleted successfully."}
        else:
            return {"message": "Permission denied. Only admins can delete users."}
