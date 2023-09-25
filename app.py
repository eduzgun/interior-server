from application import app
from application.blueprints.users.users import users_bp
from application.blueprints.auth.auth import auth_bp

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run()
