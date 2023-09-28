
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
import boto3
import os

load_dotenv()

app = Flask(__name__)
app.json_provider_class.sort_keys = False
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=100)
app.config['SESSION_COOKIE_SECURE'] = True

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
Session(app)

s3 = boto3.client('s3', region_name=os.environ["BUCKET_REGION"], aws_access_key_id=os.environ["ACCESS_KEY"], aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"])

def create_app():
    app = Flask(__name__)

    # Load the default configuration from config.py
    #app.config.from_object('application.config.Config')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
    db.init_app(app)

    # Register blueprints and extensions here
    from application.blueprints.users.users import users_bp
    from application.blueprints.rooms.rooms import rooms_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)

    return app
