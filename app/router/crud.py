from flask import url_for, redirect, session
import requests
from app.db import database
from app.db.model import Meal, User
from app.db.schema  import *
from sqlalchemy import select
from app.other.ai_service import generate_meal_details
from app.other.oauth import (
    create_access_token,
    verify_password,
    hash_password
)
from werkzeug.exceptions import NotFound, Unauthorized

def all_users():
    database.get_db()
    return database.session.execute(select(User)).scalars().all()

def get_user_by_id(id: str):
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

def get_meal_from_api(title):
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    params = {'s': title}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'meals' in data and len(data['meals']) > 0:
            meal_data = data['meals'][0]
            meal_url = url + f"meal_data['strMeal']"
            return [meal_data, meal_url]
    return None


def get_meal_from_db(title):
    database.get_db()
    return database.session.execute(select(Meal).where(Meal.title == title)).scalar_one_or_none()

def create_meal(ingredients: CreateMealForm):
    database.get_db()
    ingredients_str = ingredients.ingredients.data
    meal = generate_meal_details(ingredients_str)
    meal_description = get_meal_from_api(meal)

    db_meal = Meal(
        title=meal_description[0]['strMeal'],
        url=meal_description[1],
        user_id=session.get('user_id')
    )

    database.session.add(db_meal)
    database.session.commit()
    database.session.refresh(db_meal)
    return db_meal


def all_meals():
    database.get_db()
    return database.session.execute(select(Meal)).scalars().all()

def get_meals_by_user(user_id: str):
    database.get_db()
    return database.session.execute(select(Meal).where(Meal.user_id == user_id)).scalars().all()

def get_meal_by_id(meal_id: str):
    database.get_db()
    return database.session.get(Meal, meal_id)
