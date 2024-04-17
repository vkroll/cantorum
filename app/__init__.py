from flask import Flask
from .extensions import db, mail
from .events import events as events_blueprint
from .auth import auth as auth_blueprint
from .user import user as user_blueprint
from .main import main as main_blueprint
from flask_login import LoginManager
from .models import Login

login_manager = LoginManager()

#from .config import Config
from flask_sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    # This function is required by Flask-Login to load a user from the database
    return Login.query.get(user_id) #query.filter_by(uuid=user_id).first()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    from . import models    
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_blueprint)
    app.register_blueprint(events_blueprint, url_prefix='/events')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    #send()
    return app

