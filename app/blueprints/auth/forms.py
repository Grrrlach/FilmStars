from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, RadioField
# from wtforms.fields.core import RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from app.models import User
import random
from jinja2 import Markup
import requests
from . import bp as auth



class LoginForm(FlaskForm):
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirm_password', message="Your passwords didn't match!"), Length(min=8, message = "Your password must be at least 8 characters"), Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',  message="Your password must be at least 8 characters, and must contain a letter, a number, and a special character.")])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message="Your passwords must match.")])
    submit = SubmitField('Submit Registration!')

    # validate_form_field (email, in this case)
    #return first item in list
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email=field.data).first()
        if same_email_user:
            raise ValidationError("That email is already in use.")

class EditProfileForm(FlaskForm):

    username = StringField('Username', validators = [DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirm_password', message="Your passwords didn't match!")])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message="Your passwords didn't match!")])
    submit = SubmitField('Re-Join the Audience')