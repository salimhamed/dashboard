from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

# initialize flask extensions
# note, extensions are initalized with no Flask app instance because
# application factor is being used
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'  # use strong session protection
login_manager.login_view = 'auth.login'  # set the endpoint for login page


def create_app(config_name):
    """
    Flask Application Factory that takes configuration settings and returns
    a Flask application.
    """
    # initalize instance of Flask application
    app = Flask(__name__)

    # import configuration settings into Flask application instance
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize Flask extensions
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # register 'main' blueprint with Flask application
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register 'auth' blueprint with Flask application
    from .auth import auth as auth_blueprint
    # the 'url_prefix' parameter means all routes defined in the blueprint will
    # be registered with the prefix '/auth' (e.g., '/auth/login')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
