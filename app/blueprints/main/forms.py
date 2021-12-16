from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.widgets.core import TextArea
from app.models import User

class SearchForm(FlaskForm):
    movie_name = StringField('What is your movie called?', validators = [DataRequired()])
    movie_year = StringField('What year was it released? (YYYY)  (Not required, but helpful.)')
    submit = SubmitField('Submit')

class ReviewForm1(FlaskForm):
    title = StringField('Enter the title of your movie', validators=[DataRequired()])
    year = StringField('Enter the title of your movie', validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('Submit')

class ReviewForm2(FlaskForm):
    review_title = StringField('Say what you feel', validators = [DataRequired()])
    review_body = TextAreaField('Use your voice', validators = [DataRequired()])
    submit = SubmitField('Speak your truth')

