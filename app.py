from flask import jsonify
from application import app
from application.blueprints.users.users import users_bp
from application.blueprints.rooms.rooms import rooms_bp
from application.blueprints.likes.likes import likes_bp
from application.blueprints.auth.auth import auth_bp
from application.blueprints.filestorage.filestorage import filestorage_bp

@app.route("/")
def hello_interiordesign():
    return jsonify({
        "message": "Welcome to Interior Design API",
        "description": "Interior Design API",
        "endpoint": [
            "GET /"
        ]
    }), 200

app.register_blueprint(users_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(filestorage_bp)

if __name__ == "__main__":
    app.run()
