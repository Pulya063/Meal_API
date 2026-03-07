from flask import session
import requests
from sqlalchemy import select
from werkzeug.exceptions import NotFound, Unauthorized, Conflict

from app.db.database import get_db
from app.db.model import Meal, User
from app.db.schema import RegisterUserForm, CreateMealForm, LoginUserForm
from app.other.ai_service import generate_meal_details
from app.other.oauth import create_access_token, verify_password, hash_password


def all_users() -> list[User]:
    with get_db() as db:
        return db.execute(select(User)).scalars().all()


def get_user_by_id(user_id: str) -> User | None:
    with get_db() as db:
        return db.get(User, user_id)


def get_user_by_username(username: str) -> User | None:
    with get_db() as db:
        return db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()


def create_user(user_form: RegisterUserForm) -> User:
    existing = get_user_by_username(user_form.username.data)
    if existing is not None:
        raise Conflict(description="Username already taken")

    hashed = hash_password(user_form.password.data)

    with get_db() as db:
        db_user = User(
            username=user_form.username.data,
            password=hashed,
            birthdate=user_form.birthdate.data,
        )
        db.add(db_user)
        db.flush()
        db.refresh(db_user)
        return db_user


def login_user(user_form: LoginUserForm) -> dict:
    db_user = get_user_by_username(user_form.username.data)
    if db_user is None:
        raise NotFound(description="User not found")

    if not verify_password(user_form.password.data, db_user.password):
        raise Unauthorized(description="Incorrect password")

    access_token = create_access_token(data={"sub": db_user.user_id})
    session["user_id"] = db_user.user_id

    return {"access_token": access_token, "token_type": "bearer"}


def get_meal_from_api(title: str) -> dict | None:
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    try:
        response = requests.get(url, params={"s": title}, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("meals"):
            meal_data = data["meals"][0]
            meal_url = f"https://www.themealdb.com/meal/{meal_data['idMeal']}"
            return {"data": meal_data, "url": meal_url}
    except requests.RequestException:
        return None
    return None


def all_meals() -> list[Meal]:
    with get_db() as db:
        return db.execute(select(Meal)).scalars().all()


def get_meal_by_id(meal_id: str) -> Meal | None:
    with get_db() as db:
        return db.get(Meal, meal_id)


def get_meal_from_db(title: str) -> Meal | None:
    with get_db() as db:
        return db.execute(
            select(Meal).where(Meal.title == title)
        ).scalar_one_or_none()


def get_meals_by_user(user_id: str) -> list[Meal]:
    with get_db() as db:
        return db.execute(
            select(Meal).where(Meal.user_id == user_id)
        ).scalars().all()


def create_meal(ingredients_form: CreateMealForm) -> Meal:
    ingredients_str = ingredients_form.ingredients.data
    meal_title = generate_meal_details(ingredients_str).strip()

    meal_info = get_meal_from_api(meal_title)
    if meal_info is None:
        raise ValueError(f"Meal '{meal_title}' not found in TheMealDB")

    with get_db() as db:
        db_meal = Meal(
            title=meal_info["data"]["strMeal"],
            url=meal_info["url"],
            user_id=session.get("user_id"),
        )
        db.add(db_meal)
        db.flush()
        db.refresh(db_meal)
        return db_meal