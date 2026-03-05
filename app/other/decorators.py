from functools import wraps
from flask import url_for, redirect, flash
from requests import session


def check_user_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash("You haven`t been logged in")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper