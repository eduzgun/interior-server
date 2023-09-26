

def test_home_route(test_client):
    '''
    GIVEN a Flask app is defined
    WHEN the '/' route is requested (GET)
    THEN check that the response is valid
    '''
    response = test_client.get("/")
    assert response.status_code == 200

def test_get_user_by_id(test_client):
    '''
    GIVEN the GET /users{id} route is defined
    WHEN a user is requested by id
    THEN check that the response is valid and a username is given
    '''
    response = test_client.get('/users/1')
    assert response.status_code == 200
    assert "username" in response.json["data"]
    

def test_handle_internal_server_error(test_client):
    '''
    GIVEN the app is configured with error-handling routes
    WHEN a route that triggers an error is requestd e.g. /tupperware
    THEN check the response is an error
    '''
    response = test_client.get('/tupperware')
    assert response.status_code == 404