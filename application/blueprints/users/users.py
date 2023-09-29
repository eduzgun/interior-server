
from flask import Blueprint
from flask import jsonify, request
from werkzeug import exceptions
from application import db
from application.blueprints.users.model import Users
from application.blueprints.auth.auth import login_required

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def hello_interiordesign():
    return jsonify({
        "message": "Welcome to Interior Design API",
        "description": "Interior Design API",
        "endpoint": [
            "GET /"
        ]
    }), 200

@users_bp.route("/users/<string:name>", methods=["GET"])
def get_by_name(name):
    try:
        user = Users.query.filter_by(username=name).one()
    except:
        raise exceptions.NotFound("User not found")
    if request.method == "GET":
        return jsonify({"data":user.json}),200

@users_bp.route("/users/<int:id>", methods=['GET', 'PATCH', 'DELETE'])
@login_required
def handle_users(id):
    try:
        user = Users.query.filter_by(id=id).one()
    except:
        raise exceptions.NotFound("User not found")

    if request.method == "GET":
        return jsonify({"data": user.json}), 200
        
    if request.method == "PATCH":
        data = request.json

        for (attribute, value) in data.items():
            if hasattr(user, attribute):
                setattr(user, attribute, value)
        db.session.commit()
        return jsonify({"data": user.json }), 200
    
    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return '', 204


@users_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404


@users_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500

