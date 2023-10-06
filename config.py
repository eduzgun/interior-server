"""App configuration."""
from os import environ, path, system
from datetime import timedelta
from dotenv import load_dotenv
from application import db

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


class Config:
    """Set Flask configuration variables from .env file."""

    # General Config
    ENVIRONMENT = environ.get("ENVIRONMENT")

    # Flask Config
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    #SECRET_KEY = environ.get("SECRET_KEY")
    SECRET_KEY = '1232'
    

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SESSION_PERMANENT= True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=100)
    SESSION_COOKIE_SECURE = True
    SESSION_SQLALCHEMY = db
    CORS_HEADERS = "Content-Type"
    


class TestingConfig(Config):
    ENVIRONMENT = 'testing'
    TESTING = True
    #you can change this to add a second, testing database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = '124324'
