from flask import Blueprint
from flask import jsonify, request
from werkzeug import exceptions
from application import app, db
from application.blueprints.rooms.model import Rooms

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




@rooms_bp.route("/rooms/<int:id>", methods=['GET', 'PATCH', 'DELETE'])
def show_rooms(id):
    try:
        room = Rooms.query.filter_by(id=id).one()
    except:
        raise exceptions.NotFound("Room not found")

    if request.method == "GET":
            return jsonify({"data": room.json}), 200
        
    if request.method == "PATCH":
        data = request.json

        for (attribute, value) in data.items():
            if hasattr(room, attribute):
                setattr(room, attribute, value)
        db.session.commit()
        return jsonify({"data": room.json })
    
    if request.method == "DELETE":
        db.session.delete(room)
        db.session.commit()
        return '', 204




@rooms_bp.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return jsonify({"error": f"Ooops {err}"}),400


@rooms_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"Error message: {err}"})


@rooms_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"error": f"Opps {err}"}),500

