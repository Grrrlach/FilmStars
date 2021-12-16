from flask import render_template, request, redirect, url_for, flash
import requests
# from .forms import search_form
from .forms import LoginForm, RegisterForm, PasswordField, EditProfileForm
from wtforms.validators import EqualTo, DataRequired, ValidationError
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import bp as auth
import random
# from app import TMDB_API_KEY
TMDB_API_KEY = "eed00568b3036e632b623340bcc735b3"
# FIX TMBD - WON'T IMPORT FROM APP OR CONFIG

@auth.route('/login', methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit:
        email = request.form.get('email').lower()
        password = request.form.get('password')

        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome!', 'success')
            return redirect (url_for("main.index"))
            # main.index needs to be created.

        error_string = flash("We couldn't log you in with that email/password combo.", "danger")
        return redirect (url_for("auth.register"))

    return render_template('login.html.j2', form = form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash ("You have been logged out.", 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # build a user with form data:
            new_user_data = {
                "username":form.username.data.lower(),
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
                # "created_on":
            }

            # create new instance of empty User:
            new_user_object = User()
            # fill instance of User with data
            new_user_object.from_dict(new_user_data)

            #save user to the database:
            new_user_object.save()

            flash("Thanks for registering!", "success")

        except:
            error_string = "Something went wrong with your registration. Please try again later."
            # return for error connecting to db
            return render_template ('register.html.j2', form = form, error=error_string)
        # return for successful connection
        return redirect(url_for('auth.login'))
    # return if method on GET (first visit)
    return render_template('register.html.j2', form = form)

@auth.route('/edit_profile', methods=['GET', "POST"])
def edit_profile():
    # request.method == "GET"
    form = EditProfileForm()
    if request.method=='POST' and form.validate_on_submit():
        new_user_data={
            "username": form.username.data.lower(),
            "first_name":form.first_name.data.title(),
            "last_name":form.last_name.data.title(),
            "email":form.email.data.lower(),
            "password":form.password.data,
        }
    user=User.query.filter_by(email=form.email.data.lower()).first()
    if user and current_user.email != user.email:
        flash("Email already in use", "danger")
        return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash("Pofile Updated", "success")
        except:
            flash("Something went wrong. Please try later.", "danger")
            return redirect(url_for('auth.edit_profile'))
    return render_template('auth.edit_profile')


    # user.username = form.username.data.lower()
    # user.first_name = form.first_name.data.title()
    # user.last_name = form.last_name.data.title()
    # user.email = form.email.data.lower()
    # if form.password.data == form.confirm_password.data:
    #     user.password = form.password.data
    # else:
    #     flash("Your passwords didn't match. Please try again.", "warning")
    
        # user=User.query.filter_by(email=form.email.data.lower()).first()
        # if user and current_user.email != user.email:
        #     flash("Email already in use", "danger")
        #     return redirect(url_for('auth.edit_profile'))
        # try:
        #     current_user.from_dict(new_user_data)
        #     current_user.save()
        #     flash("Pofile Updated", "success")
        # except:
        #     random_movie_id = random.randint(1,10000)
        #     # random_movie_data = request.json()
        # while True:
        #     try:
        #         ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())["title"]
        #         random_movie_json = ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())
        #         random_movie=random_movie_json["title"]
        #         random_movie_desc = (requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json()["overview"]
        #         return f"{random_movie}:  {random_movie_desc}"
        #         flash(f'Something went wrong. Please come back later.', "danger")
        #         flash (f'In the meantime, maybe watch something?', "danger")
        #         flash (f'We might recommend {random_movie}.', "danger")
        #         flash(f'{random_movie_desc}', "danger")
        #         return redirect(url_for("auth.edit_profile"))
        #         break
        #     except:
        #             random_movie_id=random.randint(1,10000)


        
    return render_template("register.html.j2", form=form)