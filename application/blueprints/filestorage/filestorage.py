
import os
import pathlib
import zipfile
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



@filestorage_bp.route("/filestorage/environment-maps", methods=['POST'])
def handle_environment_maps():
    # if request.method == "GET":
    #     folders = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix='environment-maps/', Delimiter='/')

    #     map_tree = {}
    #     for folder in folders.get('CommonPrefixes'):
    #         folder_key = folder['Prefix']
    #         map_tree[folder_key] = []

    #         images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=folder_key)
    #         for image in images.get('Contents'):
    #             image_key = image['Key']
    #             try:
    #                 image_url = s3.generate_presigned_url('get_object', Params={'Bucket': os.environ["BUCKET_NAME"], 'Key': image_key})
    #             except:
    #                 raise exceptions.InternalServerError("Something went wrong")
            
    #             map_tree[folder_key].append(image_url)

    #     return jsonify(map_tree), 200

    if request.method == "POST":
        folder = request.form['folder']
        files = request.files.getlist("file")

        for file in files:
            try:
                s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'environment-maps/{folder}/{file.filename}')
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

        return 'Files uploaded successfully.', 201
    

@filestorage_bp.route("/filestorage/environment-maps/<string:map_name>", methods=['GET', 'PATCH', 'DELETE'])
def handle_environment_map(map_name):
    if request.method == "GET":
        images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=f'environment-maps/{map_name}')
        for image in images.get('Contents'):
            image_key = image['Key']

            try:
                # Temporary file path to store the image
                file_path = f'./tmp/{image_key.split("/")[2]}'
                folder_name = './tmp/'
                pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                
                s3.download_file(os.environ["BUCKET_NAME"], image_key, file_path)
                
                zipf = zipfile.ZipFile(f'{folder_name}images.zip','w', compression = zipfile.ZIP_STORED)
                for root, dirs, files in os.walk(folder_name):
                    for file in files:
                        zipf.write(folder_name+file)
                zipf.close()

                # Return a zip file containing the images
                return send_file(f'../{folder_name}images.zip', as_attachment=True), 200
            
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

    if request.method == "PATCH" or request.method == "DELETE":
        images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=f'environment-maps/{map_name}')

        for image in images.get('Contents'):
            image_key = image['Key']

            try:
                image_url = s3.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=image_key)
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
        if request.method == "DELETE":
            return '', 204
        
        if request.method == "PATCH":

            files = request.files.getlist("file")

            for file in files:
                try:
                    s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'environment-maps/{map_name}/{file.filename}')
                except Exception as e:
                    return f"An error occurred: {str(e)}", 500

            return 'Files updated successfully.', 201

# Delete the temporary folder and its contents
@filestorage_bp.route('/filestorage/environment-maps/cleanup', methods=['POST'])
def cleanup_temp_folder():
    try:
        for filename in os.listdir('./tmp/'):
            file_path = os.path.join('./tmp/', filename)
            os.remove(file_path)
        os.rmdir('./tmp/')
        return "", 204
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@filestorage_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"{err}"}), 404


@filestorage_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
     return jsonify({"error": f"{err}"}), 500

