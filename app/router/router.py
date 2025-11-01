from typing import List

from fastapi.security import oauth2, OAuth2PasswordRequestForm

from app.router import crud
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schema import *

router = APIRouter(prefix="/meal", tags=["meal"])

@router.get("/all_users")
def get_all_users(db: Session = Depends(get_db)):
    db_users = crud.all_users(db)
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")
    return db_users

@router.get("/user")
def get_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User haven't registered")
    return db_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login_user(db, form_data)
