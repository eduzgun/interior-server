# property-server

## running docker & pipenv

 - open docker desktop
 - run: docker run -it --rm --name lap4 --mount type=bind,src="$(pwd)",dst=/code -p 5000:5000 python:3.11 bash -c "cd /code && bash
 - pip install pipenv
 - pipenv install
 - pipenv run dev

## Endpoints for file storage API
 - **```GET ```** ```/filestorage/static-files/:image_name``` - return **```200```** status code with image url by passed image name (names are same as in your assets/images folder)
 - **```POST ```** ```/filestorage/environment-maps``` - take name of environment map (you should have **folder** form property) and all files that you want to upload to it and create folder with this name and data in cloud, return **```201```** status code
 - **```GET ```** ```/filestorage/environment-maps/:map_name``` - return **```200```** status code with zip file with images for environment map by passed name (and create **tmp** folder with images on server)
 - **```PATCH ```** ```/filestorage/environment-maps/:map_name``` - update images for environment map by passed name, return **```201```** status code (note - it deletes **ALL** images and replaces them by new, so be aware)
 - **```DELETE ```** ```/filestorage/environment-maps/:map_name``` - delete images for environment map by passed name, return **```204```** status code
 - **```POST ```** ```/filestorage/environment-maps/cleanup``` - delete **tmp** folder on server, return **```204```** status code


 ## Endpoints for authentication API
 - **```POST ```** ```/auth/register``` - take **username**, **email**, **password** form fields and create new user, return **```201```** status code with new user object (note - it generates and stores **hash** of password)
 - **```POST ```** ```/auth/login``` - take **username**, **email**, **password** form fields, check them with database data and if all good, login user and create flask session, return **```204```** status code
 - **```GET ```** ```/auth/login-check``` - check if user is logged in and have flask session, if so return **```200```** status code with user object, otherwise return **```401```** status code error (Unauthorized)
 - **```GET ```** ```/auth/logout``` - clear current user session, return **```204```** status code
 

  ## Endpoints for likes API
 - **```GET ```** ```/likes``` - return **```200```** status code with a list of all likes
 - **```POST ```** ```/likes``` - take **user_id** and **room_id** and create new like, return **```201```** status code
 - **```GET ```** ```/likes/user/:id``` - return **```200```** status code with list of likes for the specified user id
 - **```GET ```** ```/likes/room/:id``` - return **```200```** status code with list of likes for the specified room id
 - **```DELETE ```** ```/likes/:user_id/:room_id``` - delete likes by user and room id's and return **```204```** status code


   ## Endpoints for users API
 - **```GET ```** ```/users/:name``` - return **```200```** status code with a user data for the specified user name
 - **```GET ```** ```/users/:id``` - return **```200```** status code with a user data for the specified user id
 - **```PATCH ```** ```/users/:id``` - updates user by user id  with passed data and return **```204```** status code
 - **```DELETE ```** ```/users/:id``` - delete user by user id and return **```204```** status code