import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'N\xc3v\xc8.\x02p\xa4\xf0\xf2\xfaO\xef\xd2\x0c\xac\xb6\x18;\xf6\xb41\xcc\xb4'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    