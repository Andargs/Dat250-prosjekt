from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
app.config.from_object(Config)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'skvipps@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'skvipps@gmail.com'
app.config['MAIL_PASSWORD'] = 'Dromedarkrom'




db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
mail.init_app(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "30 per hour"])

from app import routes, models