from . import bp as main
from flask import render_template, request, redirect, url_for, flash
import requests
from wtforms.validators import EqualTo, DataRequired, ValidationError
from flask_login import login_user, current_user, logout_user, login_required
from . import bp as main
from app.models import Review, User
from . forms import ReviewForm1, ReviewForm2, SearchForm
import os
import random
from datetime import datetime as dt
from ..auth.routes import TMDB_API_KEY
# ABOVE IS WRONG! DON'T DO IT!!!


@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/review/<int:id>')
@login_required
def see_review (user_id):
    review = Review.query.get(user_id)
    return render_template('single_review.html.j2', review=review, view_all=True)

# @main.route('/my_reviews')
# @login_required
# def see_my_reviews():
#     all_reviews = Review.reviews_from_self(current_user)
#     return render_template('my_reviews.html.j2')

@main.route('/edit_review/<int:review_id>', methods = ['GET', 'PUT'])
@login_required
def edit_review(review_id):
    # review = Review.query.filter_by(review_id = review_id).first()
    # if review:
    #     return str(review)
    # user=User.query.filter_by(email=form.email.data.lower()).first()
    # if request.method == "PUT":
    #     new_review_data={
    #         "review_title"=form.review_title.data

    #     }
    #     review.edit(request.form.get('body'))
        
    #     flash("You have edited your review.", 'success')
    return render_template('edit_review.html.j2', review_id=review_id)

@main.route('/write_review', methods = ["GET", "POST"])
@login_required
def write_review():
    movie_name = "default"
    movie_year = "default"
    if request.method == "POST":
        movie_name = request.form.get('movie_name')
        movie_year = request.form.get('movie_year')
        review_title = request.form.get('review_title')
        review_body = request.form.get('review_body')
# ###########  IMPORTED FROM MOVIE_SEARCH()  ################
        TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
        movie_search=(requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}')).json()
        if not movie_search:
            return "We had an error loading your data. This is most likely because the title you entered is not in the database."
        movie_year = request.form.get('movie_year')
        if len(movie_search["results"])==1:
            movie_name = movie_search["results"][0]["original_title"]
            movie_year = movie_search["results"][0]["release_date"][0:4]
            movie_id = movie_search["results"][0]["id"]
        elif len(movie_search["results"])>1:
            if movie_year:
                for result in movie_search["results"]:
                    if movie_year == result["release_date"][0:4]:
                        movie_id = result["id"]
                        movie_name = result["original_title"]
                        movie_year = result["release_date"][0:4]
            else:
                movie_name=movie_search["results"][0]["original_title"]
                movie_year=movie_search["results"][0]["release_date"][0:4]
                movie_id = movie_search["results"][0]["id"]
        else:
            movie_search_error = "Please try another movie title"

        primary_movie_data = (requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}')).json()
        poster_path_suffix = primary_movie_data["poster_path"]
        poster_url=f"https://image.tmdb.org/t/p/w92{poster_path_suffix}"

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # try:
        new_review = Review(\
            user_id = current_user.user_id, \
            movie_name = movie_name, movie_year = movie_year, \
            review_title = review_title, review_body = review_body,
            movie_id = movie_id,
            poster_url = poster_url
            )
        new_review.save()
        all_reviews = Review.reviews_from_self(current_user)
        return render_template('write_review.html.j2', all_reviews=all_reviews, poster_url=poster_url)
        # except:
        #     flash("Sadly, something went wrong. Please try again", 'danger')
        #     return render_template ('write_review.html.j2')
    return render_template('write_review.html.j2')



    # if request.method == "POST":
    #     review.body(request.form.get('body'))
    #     flash("You have edited your review.", 'success')
    # return render_template('my_reviews.html.j2')
    

# @main.route('/my_movies/')
# @login_required
# def my_movies(id):

@main.route('/search', methods=['GET', 'POST'])
def search_movie():
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        # first you have to query the general movie details to get the id, using the "search" api. this returns multiple movies.
        #then IF there's a year input make sure input "year" matches year[0-4] in search results
        #take THAT movie ID and query the primary information about the movie
        # then take "runtime" and image url (prefix image with: https://image.tmdb.org/t/p/w154)

        movie_search=(requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}')).json()
        if not movie_search:
            return "We had an error loading your data. This is most likely because the title you entered is not in the database."
        year = request.form.get('year')
        if len(movie_search["results"])==1:
            movie_name = movie_search["results"][0]["original_title"]
            movie_year = movie_search["results"][0]["release_date"][0:4]
            movie_id = movie_search["results"][0]["id"]
        elif len(movie_search["results"])>1:
            if year:
                for result in movie_search["results"]:
                    if year == result["release_date"][0:4]:
                        movie_id = result["id"]
                        movie_name = result["original_title"]
                        movie_year = result["release_date"][0:4]
            else:
                movie_name=movie_search["results"][0]["original_title"]
                movie_year=movie_search["results"][0]["release_date"][0:4]
                movie_id = movie_search["results"][0]["id"]
        else:
            movie_search_error = "Please try another movie title"

        primary_movie_data = (requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}')).json()
        poster_path_suffix = primary_movie_data["poster_path"]
        poster_url=f"https://image.tmdb.org/t/p/w154{poster_path_suffix}"
        movie_runtime = primary_movie_data["runtime"]

        movie_dict={
            'movie_id': movie_id,
            'movie_name':movie_name,
            'movie_year':movie_year,
            'poster_url':poster_url,
            'movie_runtime': movie_runtime
        }

    return render_template('search.html.j2', form=form)


# @main.route('/my_movies', methods=['GET', 'POST'])
# def my_movies():
#     pass

@main.route('/my_reviews', methods=['GET'])
@login_required
def my_reviews():
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    all_reviews = Review.reviews_from_self(current_user)
    for review in all_reviews:
        movie_year = review.movie_year
        movie_name = review.movie_name
        movie_id = review.movie_id

        primary_movie_data = (requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}')).json()
        poster_path_suffix = primary_movie_data["poster_path"]
        poster_url=f"https://image.tmdb.org/t/p/w154{poster_path_suffix}"

    return render_template('write_review.html.j2', all_reviews=all_reviews, poster_url=poster_url)



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        primary_movie_data = (requests.get(f'https://api.themoviedb.org/3/movie/{Review.movie_id}?api_key={TMDB_API_KEY}')).json()
        poster_path_suffix = primary_movie_data["poster_path"]
        poster_url=f"https://image.tmdb.org/t/p/w92{poster_path_suffix}"
        # all_reviews = Review.reviews_from_self(current_user)
        return render_template('my_reviews.html.j2', all_reviews=all_reviews, poster_url=poster_url)
    except:
        return render_template ('my_reviews.html.j2')

@main.route('/review/<int:review_id>')
@login_required
def get_review(review_id):
    review = Review.query.get(review_id)
    return render_template('single_review.html.j2', review=review, view_all=True)


@main.route('/movies_to_watch')
def movies_to_watch():
    random_movie_id = random.randint(1,100000)
    # random_movie_data = request.json()
    # while ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())["title"] == None:
    while True:
        try:
            ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())["title"]
            random_movie_json = ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())
            random_movie=random_movie_json["title"]
            random_movie_desc = (requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json()["overview"]
            movie_blurb = f"{random_movie}:  {random_movie_desc}"
            # return movie_blurb
            return render_template('/includes/movies_to_watch.html.j2', movie_blurb=movie_blurb)
            break
        except:
                random_movie_id=random.randint(1,10000)

@main.route('/random_movie_gen')
def random_movie_gen():
    random_movie_id = random.randint(1,100000)
    # random_movie_data = request.json()
    # while ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())["title"] == None:
    while True:
        try:
            ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())["title"]
            random_movie_json = ((requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json())
            random_movie=random_movie_json["title"]
            random_movie_desc = (requests.get(f'https://api.themoviedb.org/3/movie/{random_movie_id}?api_key={TMDB_API_KEY}')).json()["overview"]
            movie_blurb = f"{random_movie}:  {random_movie_desc}"
            return movie_blurb
            # return render_template('/includes/movies_to_watch.html.j2', movie_blurb=movie_blurb)
            break
        except:
                random_movie_id=random.randint(1,10000)
