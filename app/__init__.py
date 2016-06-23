from flask import Flask


#from flask_mail import Mail
#from flask_moment import Moment
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config


#mail = Mail()
db = SQLAlchemy()
#moment = Moment()
bootstrap = Bootstrap()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = 'hard to guess string'

    config[config_name].init_app(app)

    db.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
  
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
   

    return app
