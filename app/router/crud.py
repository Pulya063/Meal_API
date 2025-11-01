from typing import Any
from app.db.model import Meal, User
from app.db.schema import *
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.router.oauth import (
    create_access_token,
    verify_password,
    hash_password
)

def all_users(db: Session):
    return db.query(User).all()

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: CreateUser):
    if get_user_by_username(db, user.username) is not None:
        raise HTTPException(status_code=404, detail="User not found")

    hashed = hash_password(user.password)

    db_user = User(
        username=user.username,
        password=hashed,
        date=date.today()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user: RegisterUser):
    db_user = get_user_by_username(db, user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if verify_password(user.password, db_user.password) is False:
        raise HTTPException(status_code=404, detail="Incorrect password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


