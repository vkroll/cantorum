from flask import Flask
from .extensions import db
from .events import events as events_blueprint
#from .config import Config

from flask_sqlalchemy import SQLAlchemy



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    from . import models    
    with app.app_context():
        db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(events_blueprint, url_prefix='/events')



    return app