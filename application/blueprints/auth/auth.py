import functools, os
from flask import Blueprint, jsonify, request, session, g
from werkzeug import exceptions
from application import db, s3
from sqlalchemy.exc import IntegrityError
from application.blueprints.users.model import Users
from werkzeug.security import check_password_hash, generate_password_hash


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=['POST'])
def handle_register():
    if request.method == 'POST':
        username, email, password = request.json.values()
        image_url = 'https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png'
        new_user = Users(username=username, email=email, password=generate_password_hash(password), avatar_image=image_url) 

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            if 'duplicate key value violates unique constraint \"users_username_key\"' in err.orig.args[0]:
                raise exceptions.BadRequest(f"Username {username} is already registered")
            elif 'duplicate key value violates unique constraint \"users_email_key\"' in err.orig.args[0]:
                raise exceptions.BadRequest(f"Email {email} is already registered")
            else:
                raise exceptions.InternalServerError("Something went wrong")
        
        return jsonify({"data": new_user.json}), 201
    


@auth_bp.route("/auth/login", methods=['POST'])
def handle_login():
    if request.method == 'POST':
        username, password = request.json.values()
        # username, email, password = request.json.values()

        try:
            user = Users.query.filter_by(username=username).one()
        except:
            raise exceptions.NotFound(f"User {username} is not found.")
        

        # if user.email != email: 
        #     raise exceptions.BadRequest("Incorrect email")
        # elif not check_password_hash(user.password, password):
        if not check_password_hash(user.password, password):
            raise exceptions.BadRequest("Incorrect password")
        else:
            session.pop('user_id', None)
            session['user_id'] = user.id
            return '', 204


@auth_bp.before_app_request
def before_request():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).one()


@auth_bp.route("/auth/login-check", methods=['GET'])
def login_check():
    user_id = session.get('user_id')

    if user_id is None:
        raise exceptions.Unauthorized("User is not logged in")
    else:
        try:
            user = Users.query.filter_by(id=user_id).one()
        except:
            raise exceptions.NotFound("Something whent wrong. User is not found")

        return jsonify({"data": user.json}), 200


@auth_bp.route('/auth/logout')
def logout():
    session.clear()
    return '', 204


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if g.user is None:
            raise exceptions.Unauthorized("User is not logged in")

        return func(*args, **kwargs)

    return secure_function
    

@auth_bp.errorhandler(exceptions.BadRequest)
def handle_400(err):
     return jsonify({"error": f"{err}"}), 400

@auth_bp.errorhandler(exceptions.Unauthorized)
def handle_401(err):
     return jsonify({"error": f"{err}"}), 401

@auth_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404

@auth_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500


