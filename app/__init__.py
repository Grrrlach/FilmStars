from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment, moment

login = LoginManager()
# login.login_view = 'auth.login'

db=SQLAlchemy()

migrate = Migrate()

moment = Moment()

def create_app(config_class=Config):
    app=Flask(__name__)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    # app.config.from_object(config_class)
    # SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    # TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    # I know these shouldn't ever be hard-coded,
    # and should read as above, but os.environ.get() and os.getenv() aren't grabbing
    # my whole .env file, and so far nobody has been able to figure out why
    app.config["SECRET_KEY"] = 'zMb6z86nk3Kx7PLf0MP6bcXZkqIxpzJvAqTrCP8Pb84'
    app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://kavshnys:4DuGVbmkP_SQBBgqjyVdND5c_ciOZWb0@castor.db.elephantsql.com/kavshnys"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["TMDB_API_KEY"]="eed00568b3036e632b623340bcc735b3"

    from .blueprints.main import bp as main
    app.register_blueprint(main)

    from .blueprints.auth import bp as auth
    app.register_blueprint(auth)
 
    return app

