import functools
from flask import Blueprint, flash, jsonify, request, session, g, redirect, url_for
from werkzeug import exceptions
from application import db
from application.blueprints.users.models import Users
from werkzeug.security import check_password_hash, generate_password_hash


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=['POST'])
def handle_register():
    if request.method == 'POST':
        username, email, password = request.json.values()
        new_user = Users(username=username, email=email, password=generate_password_hash(password)) 

        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            raise exceptions.BadRequest(f"Username {username} or email {email} is already registered.")
        return jsonify({"data": new_user.json}), 201
    


@auth_bp.route("/auth/login", methods=['POST'])
def handle_login():
    if request.method == 'POST':
        username, email, password = request.json.values()
        try:
            user = Users.query.filter_by(username=username).first()
        except:
            raise exceptions.NotFound(f"User {username} is not found.")

        if not check_password_hash(user.password, password):
            return jsonify({"error": "Incorrect password"}), 401
        elif user.email != email: 
            return jsonify({"error": "Incorrect email"}), 401
        else:
            session.clear()
            session['user_id'] = user.id
            return ('', 204)


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()


@auth_bp.route('/auth/logout')
def logout():
    session.clear()
    return ('', 204)


def login_required(func):
    def secure_function():
        if g.user is None:
            return  jsonify({"error": "Error message: user is not logged in"}), 400

        return func()

    return secure_function
    

@auth_bp.errorhandler(exceptions.BadRequest)
def handle_400(err):
     return jsonify({"error": f"Error message: {err}"}), 400

@auth_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"Error message: {err}"}), 404

