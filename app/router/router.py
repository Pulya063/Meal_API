from app.router import crud
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.db.database import get_db
from app.db.schema import *
from werkzeug.exceptions import HTTPException

meal = Blueprint('meal', __name__)

@meal.route('/', methods=["GET"])
def main_page():
    db = get_db()
    db_meals = crud.all_meals()
    if not db_meals:
        flash("No meals found", "error")
    return render_template('main_page.html', all_meals=db_meals)

@meal.route("/create_meal", methods=["GET", "POST"])
def create_meal():
    db = get_db()
    form = CreateMealForm()
    try:
        if request.method == "POST":
            if form.validate():
                ingredients_str = form.ingredients.data
                ingredients_list = [i.strip() for i in ingredients_str.split(',')]

                db_meal = crud.create_meal(db, form)
                if not db_meal:
                    flash("Meal haven't created", "error")
                else:
                    flash("Meal created successfully", "success")
                return render_template('get_recipe.html', form=form, meal=db_meal)
        
        return render_template('get_recipe.html', form=form)
    except Exception as e:
        flash(f"Error creating meal: {str(e)}", "error")
        return redirect(url_for('meal.create_meal'))
    finally:
        db.close()

@meal.route("/all_meals", methods=["GET"])
def get_all_meals():
    db = get_db()
    try:
        db_meals = crud.all_meals()
        if not db_meals:
            flash("No meals found", "info")
        return render_template('main_page.html', all_meals=db_meals)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('main_page.html', all_meals=[])
    finally:
        db.close()

@meal.route("/all_users", methods=["GET"])
def get_all_users():
    db = get_db()
    try:
        db_users = crud.all_users()
        if not db_users:
            flash("No users found", "info")
        return render_template('user_page.html', users=db_users)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('user_page.html', users=[])
    finally:
        db.close()

@meal.route("/user/<username>", methods=["GET"])
def get_user(username: str):
    try:
        db_user = crud.get_user_by_username(username)
        if not db_user:
            flash("User not found", "error")
            return render_template('user_page.html', user=None)
        return render_template('user_page.html', user=db_user)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('user_page.html', user=None)

@meal.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
    if request.method == "POST":
        if form.validate():
            try:
                db_user = crud.create_user(form)
                if not db_user:
                    flash("User haven't registered", "error")
                    return redirect(url_for('meal.register'))
                else:
                    flash("User registered successfully", "success")
                    return redirect(url_for('meal.login'))
            except HTTPException as e:
                flash(e.description, "error")
                return redirect(url_for('meal.register'))
        else:
            flash("Invalid form data", "error")
            return redirect(url_for('meal.register'))
    return render_template('register_page.html', form=form)

@meal.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUserForm()
    if request.method == "POST":
        if form.validate():
            try:
                result = crud.login_user(form)
                if result and "access_token" in result:
                     flash("Login successful", "success")
                     return redirect(url_for('meal.main_page'))
                else:
                    flash("Login failed", "error")
                    return redirect(url_for('meal.login'))
            except HTTPException as e:
                flash(e.description, "error")
                return redirect(url_for('meal.login'))

    return render_template('login_page.html', form=form)

@meal.route("/logout", methods=["GET"])
def logout_user():
    session.clear()
    return redirect(url_for('meal.main_page'))