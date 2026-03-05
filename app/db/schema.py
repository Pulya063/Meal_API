from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length

class CreateMealForm(FlaskForm):
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    submit = SubmitField('Create Meal')

class RegisterUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    birthdate = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
