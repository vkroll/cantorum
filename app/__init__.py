from flask import Flask
from .config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

def create_app(config_name):
    app = Flask(__name__)

    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        # Default configuration
        app.config.from_object(Config)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app