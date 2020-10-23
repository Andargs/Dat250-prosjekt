from flask import Flask, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.config import dictConfig
from logging.handlers import SMTPHandler
from flask_wtf import CSRFProtect
from flask_talisman import Talisman
<<<<<<< HEAD
#from flask_seasurf import SeaSurf
import psycopg2
import psycopg2.extras
=======
from datetime import timedelta


>>>>>>> 012ee76fed2f3b9b7d60f85a333209fa90234d27


csrf = CSRFProtect()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})



app = Flask(__name__)
#csrf = SeaSurf(app)
Talisman(app)
csp = {
    'default-src': '\'self\''
}
talisman = Talisman(app, content_security_policy=csp)
csrf.init_app(app)

app.config.from_object(Config)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'skvipps@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'skvipps@gmail.com'
app.config['MAIL_PASSWORD'] = 'Dromedarkrom'
csrf.init_app(app)





db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'relogin'
login_manager.needs_refresh_message = (u"Session timedout, please re-login")
login_manager.needs_refresh_message_category = "info"
mail = Mail(app)
mail.init_app(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "30 per hour"])

mail_handler = SMTPHandler(
    mailhost='127.0.0.1',
    fromaddr='skvipps@gmail.com',
    toaddrs=['skvipps@gmail.com'],
    subject=f'Application Error'
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))

if not app.debug:
    app.logger.addHandler(mail_handler)


from app import routes, models