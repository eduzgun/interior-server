
import os, pathlib, zipfile
from flask import Blueprint, jsonify, request, send_file
from werkzeug import exceptions
from application.blueprints.auth.auth import login_required
from application import s3


filestorage_bp = Blueprint("filestorage", __name__)

@filestorage_bp.route("/filestorage/static-files/<string:image_name>", methods=['GET'])
def get_static_image_url(image_name):
    try:
        image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': f'images/{image_name}'})
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    
    return jsonify({'image_url': image_url}), 200

@filestorage_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404


@filestorage_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500

