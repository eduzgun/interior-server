from application import app
from application.blueprints.users.users import users_bp
from application.blueprints.rooms.rooms import rooms_bp
from application.blueprints.likes.likes import likes_bp
from application.blueprints.auth.auth import auth_bp


app.register_blueprint(users_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run()
