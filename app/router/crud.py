from flask import url_for, redirect, session

from app.db import database
from app.db.model import Meal, User
from app.db.schema  import *
from sqlalchemy import select, update, insert, delete
from app.other.ai_service import generate_meal_details
from app.other.oauth import (
    create_access_token,
    verify_password,
    hash_password
)
from werkzeug.exceptions import NotFound, Conflict, Unauthorized

def all_users():
    database.get_db()
    return database.session.execute(select(User)).scalars().all()

def get_user(id: int):
    database.get_db()
    return database.session.get(User, id)

def get_user_by_username(username: str):
    database.get_db()
    return database.session.execute(select(User).where(User.username == username)).scalar_one_or_none()

def create_user(user_form: RegisterUserForm):
    database.get_db()
    if get_user_by_username(user_form.username.data) is not None:
        return redirect(url_for('meal.register'))

    hashed = hash_password(user_form.password.data)

    db_user = User(
        username=user_form.username.data,
        password=hashed,
        birthdate=user_form.birthdate.data
    )

    database.session.add(db_user)
    database.session.commit()
    database.session.refresh(db_user)
    return db_user

def login_user(user):
    db_user = get_user_by_username(user.username.data)
    if db_user is None:
        raise NotFound(description="User not found")

    if verify_password(user.password.data, db_user.password) is False:
        raise Unauthorized(description="Incorrect password")

    access_token = create_access_token(data={"sub": user.username.data})
    session['user_id'] = db_user.user_id
    return {"access_token": access_token, "token_type": "bearer"}

def create_meal(ingredients):
    database.get_db()
    ingredients_str = ingredients.ingredients.data
    details = generate_meal_details(ingredients_str)

    db_meal = Meal(
        title=details,
        description=details,
        calories=0
    )
    database.session.add(db_meal)
    database.session.commit()
    database.session.refresh(db_meal)
    return db_meal


def all_meals():
    database.get_db()
    return database.session.execute(select(Meal)).scalars().all()
