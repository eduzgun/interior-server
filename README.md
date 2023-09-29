# property-server

## running docker & pipenv

 - open docker desktop
 - run: docker run -it --rm --name lap4 --mount type=bind,src="$(pwd)",dst=/code -p 5000:5000 python:3.11 bash -c "cd /code && bash
 - pip install pipenv
 - pipenv install
 - pipenv run dev

## Endpoints for file storage API
 - ```/filestorage/static-files/<string:image_name>  GET``` - returns image url by passed image name (names are same as in your assets/images folder)
 - ```/filestorage/environment-maps GET``` - returns all environment map images in json form, name of map is key and array of URLs to 6 images is value.
 - ```/filestorage/environment-maps POST``` - take name of environment map and all files that you want to upload to it and creates folder with this name and data in cloud.
 - ```/filestorage/environment-maps/<string:map_name> GET``` - returns images for environment map by passed name
 - ```/filestorage/environment-maps/<string:map_name> PATCH``` - updates images for environment map by passed name (it deletes ALL images and replace them by new, so be aware)
 - ```/filestorage/environment-maps/<string:map_name> DELETE``` - deletes images for environment map by passed name
