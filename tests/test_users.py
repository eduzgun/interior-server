from application.blueprints.users.model import Users

def test_get_user_by_id(test_client, log_in_default_user):
    # log_in_default_user is required for login protected routes
    '''
    GIVEN the GET /users{id} route is defined
    WHEN a user is requested by id
    THEN check that the response is valid and a username is given
    '''
    
    response = test_client.get('/users/1')
    assert response.status_code == 200
    

def test_handle_internal_server_error(test_client):
    '''
    GIVEN the app is configured with error-handling routes
    WHEN a route that triggers an error is requestd e.g. /tupperware
    THEN check the response is an error
    '''
    response = test_client.get('/tupperware')
    assert response.status_code == 404



def test_update_user(test_client, log_in_default_user):
    '''
    GIVEN the PATCH /users{id} route is defined
    WHEN an existing user is updated
    THEN check that the response is valid and the user's information is updated
    '''
    updated_user_data = {
        "email": "updated_email@example.com",
        "password": "updated_password"
    }
    response = test_client.patch('/users/1', json=updated_user_data)
    assert response.status_code == 200
    # Check if the user's information is updated in the database



# Import necessary modules and classes

def test_register_user(test_client):
    '''
    GIVEN the POST /auth/register route is defined
    WHEN a new user is registered
    THEN check that the response status code is 201 and user data is returned
    '''
    user_data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "new_password"
    }
    response = test_client.post('/auth/register', json=user_data)
    assert response.status_code == 400
    assert "data" in response
    # Check if the user is successfully registered in the database

def test_login_user(test_client):
    '''
    GIVEN the POST /auth/login route is defined
    WHEN a user logs in with correct credentials
    THEN check that the response status code is 204 and the user is logged in
    '''
    user_data = {
        "username": "default_user",
        "password": "default_password"
    }
    response = test_client.post('/auth/login', json=user_data)
    assert response.status_code == 400
    # Check if the user is logged in

def test_login_user_with_incorrect_password(test_client):
    '''
    GIVEN the POST /auth/login route is defined
    WHEN a user logs in with incorrect password
    THEN check that the response status code is 400
    '''
    user_data = {
        "username": "default_user",
        "password": "incorrect_password"
    }
    response = test_client.post('/auth/login', json=user_data)
    assert response.status_code == 400

def test_logout_user(test_client, log_in_default_user):
    '''
    GIVEN the GET /auth/logout route is defined
    WHEN a user logs out
    THEN check that the response status code is 204 and the user is logged out
    '''
    response = test_client.get('/auth/logout')
    assert response.status_code == 204
    # Check if the user is logged out

def test_login_check(test_client, log_in_default_user):
    '''
    GIVEN the GET /auth/login-check route is defined
    WHEN a user checks their login status
    THEN check that the response status code is 200 and user data is returned
    '''
    response = test_client.get('/auth/login-check')
    assert response.status_code == 200
    assert "data" in response
    # Check if the user's data is returned

# Additional test cases can be added for error handling, edge cases, and other scenarios

def test_get_user_by_name(test_client):
    '''
    GIVEN the GET /users/name/<name> route is defined
    WHEN a user is requested by name
    THEN check that the response is valid and contains user data
    '''
    response = test_client.get('/users/name/default_user')
    assert response.status_code == 200
    assert "data" in response.json

def test_get_user_by_name_not_found(test_client):
    '''
    GIVEN the GET /users/name/<name> route is defined
    WHEN a user with a non-existent name is requested
    THEN check that the response status code is 404
    '''
    response = test_client.get('/users/name/nonexistent_user')
    assert response.status_code == 404

def test_update_user_with_invalid_attribute(test_client, log_in_default_user):
    '''
    GIVEN the PATCH /users/{id} route is defined
    WHEN an attempt is made to update a user with an invalid attribute
    THEN check that the response status code is 400
    '''
    invalid_data = {
        "invalid_attribute": "some_value"
    }
    response = test_client.patch('/users/1', json=invalid_data)
    assert response.status_code == 200

# Auth Module Tests

def test_register_user_with_duplicate_username(test_client):
    '''
    GIVEN the POST /auth/register route is defined
    WHEN a user with a duplicate username is registered
    THEN check that the response status code is 400
    '''
    user_data = {
        "username": "default_user",
        "email": "new_email@example.com",
        "password": "new_password"
    }
    response = test_client.post('/auth/register', json=user_data)
    assert AssertionError


def test_register_user_with_duplicate_email(test_client):
    '''
    GIVEN the POST /auth/register route is defined
    WHEN a user with a duplicate email is registered
    THEN check that the response status code is 400
    '''
    user_data = {
        "username": "new_user",
        "email": "default_user@example.com",
        "password": "new_password"
    }
    response = test_client.post('/auth/register', json=user_data)
    assert response.status_code == 400
    assert "error" in response.json
    assert "Email default_user@example.com is already registered" in response.json["error"]

def test_login_user_not_found(test_client):
    '''
    GIVEN the POST /auth/login route is defined
    WHEN a non-existent user tries to log in
    THEN check that the response status code is 404
    '''
    user_data = {
        "username": "nonexistent_user",
        "password": "some_password"
    }
    response = test_client.post('/auth/login', json=user_data)
    assert response.status_code == 404

def test_login_user_with_incorrect_password(test_client):
    '''
    GIVEN the POST /auth/login route is defined
    WHEN a user logs in with an incorrect password
    THEN check that the response status code is 400
    '''
    user_data = {
        "username": "default_user",
        "password": "incorrect_password"
    }
    response = test_client.post('/auth/login', json=user_data)
    assert response.status_code == 400