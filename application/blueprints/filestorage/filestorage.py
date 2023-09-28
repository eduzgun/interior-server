
import os
from flask import Blueprint
from flask import jsonify, request
from werkzeug import exceptions
from application.blueprints.auth.auth import login_required
from application import s3


filestorage_bp = Blueprint("filestorage", __name__)

@filestorage_bp.route("/filestorage/static-files/<string:image_name>", methods=['GET'])
def get_static_image_url(image_name):
    try:
        image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': f'images/{image_name}'})
    except:
        raise exceptions.InternalServerError("Something went wrong")
    
    return jsonify({'image_url': image_url}), 200



@filestorage_bp.route("/filestorage/enviroment-maps", methods=['GET','POST'])
def handle_enviroment_maps():
    if request.method == "GET":
        folders = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix='enviroment-maps/', Delimiter='/')

        map_tree = {}
        for folder in folders.get('CommonPrefixes'):
            folder_key = folder['Prefix']
            map_tree[folder_key] = []

            images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=folder_key)
            for image in images.get('Contents'):
                image_key = image['Key']
                try:
                    image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': image_key})
                except:
                    raise exceptions.InternalServerError("Something went wrong")
            
                map_tree[folder_key].append(image_url)

        return jsonify(map_tree), 200

    if request.method == "POST":
        folder = request.form['folder']
        files = request.files.getlist("file")

        for file in files:
            try:
                s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'enviroment-maps/{folder}/{file.filename}')
            except:
                raise exceptions.InternalServerError("Something went wrong")

        return 'Files uploaded successfully.', 201
    

@filestorage_bp.route("/filestorage/enviroment-maps/<string:map_name>", methods=['GET', 'PATCH', 'DELETE'])
def handle_enviroment_map(map_name):
    if request.method == "GET":
        map_tree = {}
        images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=f'enviroment-maps/{map_name}')

        for image in images.get('Contents'):
            image_key = image['Key']

            try:
                image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': image_key})
            except:
                raise exceptions.InternalServerError("Something went wrong")
            
            map_tree[image_key.split('/')[2]] = image_url

        return jsonify(map_tree), 200
    
    if request.method == "PATCH" or request.method == "DELETE":
        images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=f'enviroment-maps/{map_name}')

        for image in images.get('Contents'):
            image_key = image['Key']

            try:
                image_url = s3.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=image_key)
            except:
                raise exceptions.InternalServerError("Something went wrong")
            
        if request.method == "DELETE":
            return '', 204
        
        if request.method == "PATCH":

            files = request.files.getlist("file")

            for file in files:
                try:
                    s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'enviroment-maps/{map_name}/{file.filename}')
                except:
                    raise exceptions.InternalServerError("Something went wrong")

            return 'Files updated successfully.', 201


@filestorage_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404


@filestorage_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500

