
import os
from flask import Blueprint, jsonify, request
from werkzeug import exceptions
from application import s3, db
from application.blueprints.users.model import Users
from application.blueprints.rooms.model import Rooms
from application.blueprints.auth.auth import login_required


filestorage_bp = Blueprint("filestorage", __name__)

@filestorage_bp.route("/filestorage/avatar-images/<int:user_id>", methods=['POST', 'PATCH', 'DELETE'])
@login_required
def get_avatar_image_url(user_id):
    try:
        user = Users.query.filter_by(id=user_id).one()
    except:
        raise exceptions.NotFound("User not found")
    
    file = request.files['file']
    
    if request.method == "POST":
        try:
            s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'avatar-images/{user_id}')
            image_url = f'https://interior-cloud-store.s3.amazonaws.com/avatar-images/{user_id}'
            setattr(user, user.avatar_image, image_url)
            db.session.commit()
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

        return 'Avatar uploaded successfully', 201
    
    if request.method == "PATCH" or request.method == "DELETE":
        try:
            s3.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=f'avatar-images/{user_id}')
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

        if request.method == "DELETE":
            try:
                image_url = 'https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png'
                setattr(user, user.avatar_image, image_url)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
            return '', 204


        if request.method == "PATCH":
            try:
                s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'avatar-images/{user_id}')
                image_url = f'https://interior-cloud-store.s3.amazonaws.com/avatar-images/{user_id}'
                setattr(user, user.avatar_image, image_url)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

        return 'Avatar updated successfully', 200
    

@filestorage_bp.route("/filestorage/room-images/<string:room_name>", methods=['POST', 'PATCH', 'DELETE'])
@login_required
def get_room_image_url(room_name):
    try:
        room = Rooms.query.filter_by(name=room_name).one()
    except:
        raise exceptions.NotFound("Room not found")
    
    file = request.files['file']
    
    if request.method == "POST":
        try:
            s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'room-images/{room_name}')
            image_url = f'https://interior-cloud-store.s3.amazonaws.com/room-images/{room_name}'
            setattr(room, room.cover_image, image_url)
            db.session.commit()
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

        return 'Room image uploaded successfully', 201
    
    if request.method == "PATCH" or request.method == "DELETE":
        try:
            s3.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=f'room-images/{room_name}')
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

        if request.method == "DELETE":
            try:
                image_url = f'https://interior-cloud-store.s3.amazonaws.com/environment-maps/{room_name}/px.png'
                setattr(room, room.cover_image, image_url)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
            return '', 204


        if request.method == "PATCH":
            try:
                s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'room-images/{room_name}')
                image_url = f'https://interior-cloud-store.s3.amazonaws.com/room-images/{room_name}'
                setattr(room, room.cover_image, image_url)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

        return 'Room image updated successfully', 200

@filestorage_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404


@filestorage_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500

