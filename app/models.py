from app import db
from sqlalchemy import Sequence, or_
from flask_login import UserMixin
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import requests
import secrets

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    # movies_watched = db.relationship ('Movie', backref='watched_by', lazy=True)
    movie_reviews = db.relationship('Review', backref='author', lazy='dynamic')

    token = db.Column(db.String, index = True, unique=True)
    token_exp = db.Column (db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)


    #salt and hash
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    # end salt and hash

    def from_dict(self, data):
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        # self.created_on = data['created_on']
        # self.movies_watched = data['movies_watched']
        # self.reviews = data['reviews']

    #token Auth
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        #if no current valid token:
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token (self):
        self.token_exp = dt.utcnow() - timedelta(seconds = 61)
    
    @staticmethod
    def check_token (token):
        u = User.query.filter_by(token = token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

    #get review user wrote
    def reviews(self):
        self_reviews = Review.query.filter_by(user_id = self.id)

    def get_id(self):
        return (self.user_id)

    #save the user to the database
    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_my_reviews(self):
        my_reviews = Review.query.filter_by(user_id=self.id)
        my_reviews_ordered = my_reviews.order_by(Review.created_on.desc())
        return my_reviews_ordered

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    movie_name = db.Column(db.String)
    movie_year = db.Column(db.String)
    review_body = db.Column(db.Text)
    review_title = db.Column(db.String(50))
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date_created = db.Column(db.DateTime, default=dt.utcnow())
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow())
    poster_url = db.Column(db.String)
    reviews = db.relationship('User', backref='reviews')
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def edit(self, new_body):
        self.body=new_body
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
        self.title = data['review_title']
        self.review_body = data['review_body']

    def reviews_from_self(current_user):
        reviews_user_wrote = Review.query.filter_by(user_id=current_user.user_id).order_by('date_created')
        return reviews_user_wrote
        # Review.query.filter_by(user_id =self.user_id)
        # Review.query.filter(or_(user_id =self.user_id, movie_name = self.movie_name))
        # query.filter(or_(User.name == 'ed', User.name == 'wendy'))

        # db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))


        # (or_(user_id ==self.user_id, db.movie_name == self.movie_name))

    def __repr__(self):
        return f'<id:{self.user_id} | Review: {self.review_body[:30]}>'
