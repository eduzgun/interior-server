
from flask import Blueprint, render_template, redirect
from flask import jsonify, request
from werkzeug import exceptions
from application import app, db
from application.blueprints.users.model import Users



users_bp = Blueprint("users", __name__)


@users_bp.route("/")
def hello_interiordesign():
    return jsonify({
        "message": "Welcome",
        "description": "Interior Design API",
        "endpoint": [
            "GET /"
        ]
    }), 200



@users_bp.route("/users", methods=["GET"])
def handle_users():
    if request.method == "GET":
        try:
            users = Users.query.all()
            data = [u.json for u in users]
            return jsonify({"users": data})
        except:
            raise exceptions.InternalServerError("We are working on it ")

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




# @app.route("/series/<int:id>", methods=['GET', 'PATCH', 'DELETE'])
# def show_series(id):
#     if request.method == "GET":
#         try:
#             series = Series.query.filter_by(id=id).first()
#             return jsonify({"data": series.json}), 200
#         except:
#             raise exceptions.NotFound("Series not found")
        
#     if request.method == "PATCH":
#         data = request.json
#         series = Series.query.filter_by(id=id).first()

#         for (attribute, value) in data.items():
#             if hasattr(series, attribute):
#                 setattr(series, attribute, value)
#         db.session.commit()
#         return jsonify({"data": series.json })
    
#     if request.method == "DELETE":
#         series = Series.query.filter_by(id=id).first()
#         db.session.delete(series)
#         db.session.commit()
#         return f"Series Deleted", 204




# @app.errorhandler(exceptions.BadRequest)
# def handle_400(err):
#     return jsonify({"error": f"Ooops {err}"}),400


# @app.errorhandler(exceptions.NotFound)
# def handle_404(err):
#     return jsonify({"error": f"Error message: {err}"})


@users_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"error": f"Opps {err}"}),500

