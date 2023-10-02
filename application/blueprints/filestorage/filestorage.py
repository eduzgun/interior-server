
import os
from flask import Blueprint, jsonify, request
from werkzeug import exceptions
from application import s3, db
from application.blueprints.users.model import Users
from application.blueprints.auth.auth import login_required


filestorage_bp = Blueprint("filestorage", __name__)

@filestorage_bp.route("/filestorage/static-files/<string:image_name>", methods=['GET'])
def get_static_image_url(image_name):
    try:
        image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': f'images/{image_name}'})
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    
    return jsonify({'image_url': image_url}), 200

@filestorage_bp.route("/filestorage/avatar-images/<int:id>", methods=['POST', 'PATCH', 'DELETE'])
@login_required
def get_avatar_image_url(id):
    try:
        user = Users.query.filter_by(id=id).one()
    except:
        raise exceptions.NotFound("User not found")
    
    if request.method == "POST":
        file_ref = request.files
        file = request.files[file_ref]
        try:
            s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'avatar-images/{id}')
            image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': f'avatar-images/{id}'})
            setattr(user, user.avatar_image, image_url)
            db.session.commit()
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

        return 'Avatar uploaded successfully', 201
    
    if request.method == "PATCH" or request.method == "DELETE":
        try:
            s3.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=f'avatar-images/{id}')
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

        if request.method == "DELETE":
            try:
                image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': f'avatar-images/default.png'})
                setattr(user, user.avatar_image, image_url)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
            return 'Avatar deleted successfully', 201


        if request.method == "PATCH":
            file_ref = request.files
            file = request.files[file_ref]
            try:
                s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'avatar-images/{id}')
                image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': f'avatar-images/{id}'})
                setattr(user, user.avatar_image, image_url)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

        return 'Avatar updated successfully', 201

@filestorage_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404


@filestorage_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500

