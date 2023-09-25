
from flask import Blueprint
from flask import jsonify, request
from werkzeug import exceptions
from application import db
from application.blueprints.users.models import Users
from application.blueprints.auth.auth import login_required


users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def hello_interiordesign():
    return jsonify({
        "message": "Users root endpoint",
        "description": "Interior Design API",
        "endpoint": [
            "GET /"
        ]
    }), 200



@users_bp.route("/users/<int:id>", methods=['GET', 'PATCH', 'DELETE'])
@login_required
def handle_users(id):
    try:
        user = Users.query.filter_by(id=id).first()
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
        return jsonify({"data": user.json })
    
    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return f"User Deleted", 204

# 
#     if request.method == "POST":
#         try:
#             name, start_date, end_date, country, network = request.json.values()
#             new_series = Series(name=name, start_date=start_date, end_date=end_date, country=country, network=network) 

#             db.session.add(new_series)
#             db.session.commit()
#             return jsonify({"data": new_series.json}), 201
#         except:
#             raise exceptions.BadRequest(f"We cannot process your request, name, start_date, end_date, country, network are required")




# @app.errorhandler(exceptions.BadRequest)
# def handle_400(err):
#     return jsonify({"error": f"Ooops {err}"}),400


@users_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"Error message: {err}"}), 404


@users_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"Error message: {err}"}), 500

