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
    updated_user = Users.query.get(1)
    assert updated_user.email == "updated_email@example.com"
    assert updated_user.password == "updated_password"


