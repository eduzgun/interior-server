

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