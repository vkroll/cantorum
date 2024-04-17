class Config:
    # Base configuration settings
    MY_CHOIR = 'INSERT CHOIRNAME HERE'
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'database_uri_here'

    # ... other base config settings

class DevelopmentConfig(Config):
    # Development-specific settings
    DEBUG = True
    # ... other development config settings

class TestingConfig(Config):
    # Testing-specific settings
    TESTING = True
    # ... other testing config settings

class ProductionConfig(Config):
    # Production-specific settings
    DEBUG = False
    # ... other production config settings
