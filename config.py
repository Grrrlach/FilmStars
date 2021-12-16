import os
class Config():
    # I know these shouldn't ever be hard-coded,
    # and should only be explicit in my .env
    # see my init for explanation
    SECRET_KEY = 'zMb6z86nk3Kx7PLf0MP6bcXZkqIxpzJvAqTrCP8Pb84'
    SQLALCHEMY_DATABASE_URI='postgresql://kavshnys:4DuGVbmkP_SQBBgqjyVdND5c_ciOZWb0@castor.db.elephantsql.com/kavshnys'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    TMDB_API_KEY = 'eed00568b3036e632b623340bcc735b3'