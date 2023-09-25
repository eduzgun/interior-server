import datetime
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.json_provider_class.sort_keys = False
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=1)
app.config['SESSION_COOKIE_SECURE'] = True

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

Session(app)