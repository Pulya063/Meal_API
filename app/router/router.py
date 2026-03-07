from app.other.decorators import check_user_access
from app.router import crud
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.db.schema import *
from werkzeug.exceptions import HTTPException

meal = Blueprint('meal', __name__)


@meal.route('/', methods=["GET"])
def main_page():
    form = CreateMealForm()
    return render_template('main_page.html', form=form)

@meal.route("/create_meal", methods=["GET", "POST"])
@check_user_access
def create_meal():
    form = CreateMealForm()
    try:
        if request.method == "POST":
            if form.validate():
                db_meal = crud.create_meal(form)
                if db_meal is None:
                    raise Exception("Meal haven't created", "error")
                else:
                    flash("Meal created successfully", "success")
                    return render_template('get_recipe.html', form=form, meal=db_meal)
            else:
                raise Exception("Invalid form data", "error")

        return render_template('get_recipe.html', form=form)
    except Exception as e:
        flash(f"Error creating meal: {str(e)}", "error")
        return redirect(url_for('meal.create_meal'))


@meal.route("/all_meals", methods=["GET"])
@check_user_access
def get_all_meals():
    try:
        db_meals = crud.all_meals()
        if not db_meals:
            raise Exception("No meals found", "error")
        return render_template('main_page.html', all_meals=db_meals)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('main_page.html', all_meals=[])


@meal.route("/all_users", methods=["GET"])
@check_user_access
def get_all_users():
    try:
        db_users = crud.all_users()
        if not db_users:
            flash("No users found", "info")
        return render_template('user_page.html', users=db_users)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('user_page.html', users=[])


@meal.route("/user/<user_id>", methods=["GET"])
@check_user_access
def get_user(user_id: str):
    try:
        db_user = crud.get_user_by_id(user_id)
        if not db_user:
            flash("User not found", "error")
            return render_template('user_page.html', user=None)
        return render_template('user_page.html', user=db_user)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('user_page.html', user=None)

@meal.route("/user/<user_id>/meals", methods=["GET"])
@check_user_access
def get_user_meals(user_id: str):
    try:
        db_meals = crud.get_meals_by_user(user_id)
        if not db_meals:
            flash("No meals found for this user", "error")
        return render_template('user_meals.html', meals=db_meals)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('user_meals.html', meals=[])

@meal.route("/meal/<meal_id>", methods=["GET"])
@check_user_access
def get_meal_detail(meal_id: str):
    try:
        db_meal = crud.get_meal_by_id(meal_id)
        if not db_meal:
            flash("Meal not found", "error")
            return redirect(url_for('meal.main_page'))
        return render_template('meal_detail.html', meal=db_meal)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('meal.main_page'))

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
