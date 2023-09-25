from flask import Blueprint, render_template, redirect
from flask import jsonify, request
from werkzeug import exceptions
from application import app, db
from application.blueprints.rooms.model import Rooms

# room_name = db.Column(db.String(100), nullable=False)
#     room_dimensions = db.Column(db.Integer, nullable=False)
#     room_description = db.Column(db.String(100), nullable=False)
#     room_theme = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

rooms_bp = Blueprint("rooms", __name__)


@rooms_bp.route("/rooms", methods=['GET', 'POST'])
def handle_rooms():
    if request.method == "GET":
        try:
            rooms = Rooms.query.all()
            data = [r.json for r in rooms]
            return jsonify({"rooms": data})
        except:
            raise exceptions.InternalServerError("We are working on it ")


    if request.method == "POST":
        try:
            name, dimensions, description, theme, user_id = request.json.values()
            new_room = Rooms(name=name, dimensions=dimensions, description=description, theme=theme, user_id=user_id) 

            db.session.add(new_room)
            db.session.commit()
            return jsonify({"data": new_room.json}), 201
        except:
            raise exceptions.BadRequest(f"We cannot process your request: name, dimensions, description, theme, user_id are required")




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




@rooms_bp.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return jsonify({"error": f"Ooops {err}"}),400


# @app.errorhandler(exceptions.NotFound)
# def handle_404(err):
#     return jsonify({"error": f"Error message: {err}"})


@rooms_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"error": f"Opps {err}"}),500

