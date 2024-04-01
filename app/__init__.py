from flask import Flask
from .extensions import db
from .events import events as events_blueprint
from .auth import auth as auth_blueprint
from .main import main as main_blueprint
#from .config import Config

from flask_sqlalchemy import SQLAlchemy



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    from . import models    
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_blueprint)
    app.register_blueprint(events_blueprint, url_prefix='/events')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')



    return app