from flask import Blueprint
from flask import jsonify, request
from werkzeug import exceptions
from application import db
from application.blueprints.users.model import Likes


likes_bp = Blueprint("likes", __name__)


@likes_bp.route("/likes", methods=['GET', 'POST'])
def handle_likes():
    if request.method == "GET":
        try:
            likes = Likes.query.all()
            data = [l.json for l in likes]
            return jsonify({"likes": data})
        except:
            raise exceptions.InternalServerError("We are working on it ")


    if request.method == "POST":
        
        user_id, room_id = request.json.values()

        if Likes.query.filter_by(user_id=user_id, room_id=room_id).first():
            raise exceptions.BadRequest("This user already liked this room")

        try:    
            new_like = Likes(user_id=user_id, room_id=room_id) 
            db.session.add(new_like)
            db.session.commit()
            return jsonify({"data": new_like.json}), 201
        except:
            raise exceptions.InternalServerError("Something went wrong")




@likes_bp.route("/likes/user/<int:id>", methods=['GET'])
def show_likes_user(id):
    if request.method == "GET":
        likes = Likes.query.filter_by(user_id=id).all()
        data = [l.json for l in likes]

        if not data:
            raise exceptions.NotFound("Likes not found for this user")
        
        return jsonify({"data": data}), 200
            


@likes_bp.route("/likes/room/<int:id>", methods=['GET'])
def show_likes_room(id):
    if request.method == "GET":
        likes = Likes.query.filter_by(room_id=id).all()
        data = [l.json for l in likes]

        if not data:
            raise exceptions.NotFound("Likes not found for this room")

        return jsonify({"data": data}), 200


@likes_bp.route("/likes/<int:user_id>/<int:room_id>", methods=['DELETE'])
def delete_likes_room(user_id, room_id):
    if request.method == "DELETE":
        try:
            like = Likes.query.filter_by(user_id=user_id, room_id=room_id).one()
        except:
            raise exceptions.NotFound("Like for this user and room is not found")
        
        db.session.delete(like)
        db.session.commit()
        return '', 204


@likes_bp.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return jsonify({"error": f"{err}"}),400


@likes_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"})


@likes_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"error": f"{err}"}),500

