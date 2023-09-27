from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()

# Define extensions without attaching them to the app yet

app = Flask(__name__)
app.json_provider_class.sort_keys = False
CORS(app)
# Initialize SQLAlchemy outside of create_app
db = SQLAlchemy(app)

# Configure the Flask app inside create_app

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=100)
app.config['SESSION_COOKIE_SECURE'] = True

# Initialize extensions within the create_app function


# Register blueprints and extensions here
from application.blueprints.users.users import users_bp
from application.blueprints.rooms.rooms import rooms_bp
from application.blueprints.auth.auth import auth_bp
from application.blueprints.likes.likes import likes_bp

app.register_blueprint(users_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(likes_bp)

Session(app)

# Usage example:
# if __name__ == "__main__":
#     app = create_app()
#     app.run()
