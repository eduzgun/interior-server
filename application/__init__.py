from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
import boto3
import os

from click import echo
load_dotenv()

db = SQLAlchemy()


s3 = boto3.client('s3', region_name=os.environ["BUCKET_REGION"], aws_access_key_id=os.environ["ACCESS_KEY"], aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"])

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    #configure as default from config.py
    app.config.from_object('config.Config')
    app.json_provider_class.sort_keys = False
    CORS(app)

    @app.route("/")
    def hello_interiordesign():
        return jsonify({
            "message": "Welcome to Interior Design API",
            "description": "Interior Design API",
            "endpoint": [
                "GET /"
            ]
        }), 200


    db.init_app(app)

    with app.app_context():
        # Register blueprints and extensions here
        from application.blueprints.users.users import users_bp
        from application.blueprints.rooms.rooms import rooms_bp
        from application.blueprints.auth.auth import auth_bp
        from application.blueprints.likes.likes import likes_bp
        from application.blueprints.filestorage.filestorage import filestorage_bp

        app.register_blueprint(users_bp)
        app.register_blueprint(rooms_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(likes_bp)
        app.register_blueprint(filestorage_bp)
    
        
        db.create_all()
        return app


