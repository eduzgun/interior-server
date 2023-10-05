#from flask import current_app
import os, pathlib, zipfile
from application import s3
from flask import Blueprint, send_file
from flask import jsonify, request
from werkzeug import exceptions
from application import db
from application.blueprints.rooms.model import Rooms
from application.blueprints.auth.auth import login_required

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
        # upload room files to s3 storage
        files = request.files
        form_name = request.form.get("name")
        positions = ["px","nx","py","ny","pz","nz"]
        for count, file in enumerate(files):
            x = files[file]
            try:
                s3.upload_fileobj(x, os.environ["BUCKET_NAME"], f'environment-maps/{form_name}/{positions[count]}')
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
        try:
            name = request.form.get("name")
            dimensions = request.form.get("dimensions")
            description = request.form.get("description")
            theme = request.form.get("theme")
            category = request.form.get("category")
            cover_image = f'https://interior-cloud-store.s3.amazonaws.com/environment-maps/{name}/px.png'
            user_id = request.form.get("user_id")

            new_room = Rooms(name=name, dimensions=dimensions, description=description, theme=theme, category=category, cover_image=cover_image, user_id=user_id) 

            db.session.add(new_room)
            db.session.commit()
        except Exception as e:
                return f"An error occurred: {str(e)}", 400

        return jsonify({"data": new_room.json}), 201





@rooms_bp.route("/rooms/<int:id>", methods=['GET', 'PATCH', 'DELETE'])
def show_rooms(id):
    try:
        room = Rooms.query.filter_by(id=id).one()
    except:
        raise exceptions.NotFound("Room not found")

    if request.method == "GET":
            return jsonify({"data": room.json}), 200
    
    if request.method == "PATCH" or request.method == "DELETE":
        images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=f'environment-maps/{room.name}')

        for image in images.get('Contents'):
            image_key = image['Key']

            try:
                s3.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=image_key)
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
        if request.method == "DELETE":
            try:
                db.session.delete(room)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
            
            return '', 204
        
        if request.method == "PATCH":
            data = request.json

            try:
                for (attribute, value) in data.items():
                    if hasattr(room, attribute):
                        setattr(room, attribute, value)
                db.session.commit()
            except Exception as e:
                    return f"An error occurred: {str(e)}", 500

            files = request.files.getlist("file")

            for file in files:
                try:
                    s3.upload_fileobj(file, os.environ["BUCKET_NAME"], f'environment-maps/{room.name}/{file.filename}')
                except Exception as e:
                    return f"An error occurred: {str(e)}", 500

            return jsonify({"data": room.json }), 200
        


@rooms_bp.route("/rooms/images/<int:id>", methods=['GET'])
def handle_environment_map(id):
    if request.method == "GET":
        try:
            room = Rooms.query.filter_by(id=id).one()
        except:
            raise exceptions.NotFound("Room not found")

        images = s3.list_objects_v2(Bucket=os.environ["BUCKET_NAME"], Prefix=f'environment-maps/{room.name}')
        for image in images.get('Contents'):
            image_key = image['Key']

            try:
                # Temporary file path to store the image
                file_path = f'./tmp/{image_key.split("/")[2]}'
                folder_name = './tmp/'

                pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                s3.download_file(os.environ["BUCKET_NAME"], image_key, file_path)
                
            except Exception as e:
                return f"An error occurred: {str(e)}", 500
        try:        
            zipf = zipfile.ZipFile(f'{folder_name}images.zip','w', compression = zipfile.ZIP_STORED)
            for root, dirs, files in os.walk(folder_name):
                for file in files[1:]:
                    zipf.write(folder_name+file)
            zipf.close()

            # Return a zip file containing the images
            return send_file(f'../{folder_name}images.zip', as_attachment=True), 200
        except Exception as e:
                return f"An error occurred: {str(e)}", 500
                
        


# Delete the temporary folder and its contents
@rooms_bp.route('/rooms/images/cleanup', methods=['POST'])
def cleanup_temp_folder():
    try:
        for filename in os.listdir('./tmp/'):
            file_path = os.path.join('./tmp/', filename)
            os.remove(file_path)
        os.rmdir('./tmp/')
        return "", 204
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



@rooms_bp.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return jsonify({"error": f"Ooops {err}"}),400


@rooms_bp.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"error": f"Error message: {err}"})


@rooms_bp.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"error": f"Opps {err}"}),500

