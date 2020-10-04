from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message


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

from app import routes, models