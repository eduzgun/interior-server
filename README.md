# property-server

## running docker & pipenv

 - open docker desktop
 - run: docker run -it --rm --name lap4 --mount type=bind,src="$(pwd)",dst=/code -p 5000:5000 python:3.11 bash -c "cd /code && bash
 - pip install pipenv
 - pipenv install
 - pipenv run dev

## Endpoints for file storage API
 - **```GET```** ```/filestorage/static-files/:image_name``` - return **```200```** status code with image url by passed image name (names are same as in your assets/images folder)
 - **```POST```** ```/filestorage/avatar-images/:user_id``` - return **```201```** status code, upload avatar image for user on s3 and change link for avatar image in user table. Pass user id in params.
 - **```PATCH```** ```/filestorage/avatar-images/:user_id``` - return **```201```** status code, delete previous avatar image on s3 and change for new one, update link for avatar image in user table. Pass user id in params.
 - **```DELETE```** ```/filestorage/avatar-images/:user_id``` - return **```204```** status code, delete avatar image and change link for avatar image in user table for default one. Pass user id in params.


## Endpoints for authentication API
 - **```POST```** ```/auth/register``` - return **```201```** status code, take **username**, **email**, **password** form fields and create new user create and return new user object with default avatar image link (note - it generates and stores **hash** of password)
 - **```POST```** ```/auth/login``` - return **```204```** status code, take **username**, **password** form fields, check them with database data and if all good, login user and create flask session
 - **```GET```** ```/auth/login-check``` - check if user is logged in and have flask session, if so return **```200```** status code with user object, otherwise return **```401```** status code error (Unauthorized)
 - **```GET```** ```/auth/logout``` - return **```204```** status code, clear current user session
 

## Endpoints for likes API
 - **```GET```** ```/likes``` - return **```200```** status code with a list of all likes
 - **```POST```** ```/likes``` - return **```201```** status code, take **user_id** and **room_id** and create new like
 - **```GET```** ```/likes/user/:id``` - return **```200```** status code with list of likes for the specified user id
 - **```GET```** ```/likes/room/:id``` - return **```200```** status code with list of likes for the specified room id
 - **```DELETE```** ```/likes/:user_id/:room_id``` - return **```204```** status code and delete likes by user and room id's


## Endpoints for users API
 - **```GET```** ```/users/name/:name``` - return **```200```** status code with a user data for the specified user name
 - **```GET```** ```/users/:id``` - return **```200```** status code with a user data for the specified user id
 - **```PATCH```** ```/users/:id``` - return **```201```** status code, update user by user id with passed data and return updated user data
 - **```DELETE```** ```/users/:id``` - return **```204```** status code, delete user by user id


## Endpoints for rooms API
 - **```GET```** ```/rooms``` - return **```200```** status code and list of all rooms from rooms table.
 - **```POST```** ```/rooms``` - return **```201```** status code, create new db row in rooms table and then take name of room with all files that you want to upload to it and create folder with this name and data in s3 cloud
 - **```GET```** ```/rooms/images/:id``` - return **```200```** status code with zip file with images for environment map by passed room id (and create **tmp** folder with images on server)
 - **```POST```** ```/rooms/images/cleanup``` - return **```204```** status code and delete **tmp** folder on server
 - **```GET```** ```/rooms/:id``` - return **```200```** status code and room data from rooms table selected by passed room id
 - **```PATCH```** ```/rooms/:id``` - return **```201```** status code, update room record in rooms table and images for environment map on s3 cloud by passed room id (note - it deletes **ALL** images and replaces them by new, so be aware)
 - **```DELETE```** ```/rooms/:id``` - return **```204```** status code and delete room record in rooms table with images for environment map by passed room id
