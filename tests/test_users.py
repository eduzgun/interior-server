

def test_home_route(test_client):
    '''
    GIVEN a Flask app is defined
    WHEN the '/' route is requested (GET)
    THEN check that the response is valid
    '''
    response = test_client.get("/")
    assert response.status_code == 200

def test_get_all_users(test_client):
    '''
    GIVEN the GET /users route is defined
    WHEN the '/users' page is requested (GET)
    THEN check that the response is valid
    '''
    response = test_client.get('/users')
    assert response.status_code == 200
    

def test_handle_internal_server_error(test_client):
    '''
    GIVEN the app is configured with error-handling routes
    WHEN a route that triggers an error is requestd e.g. /tupperware
    THEN check the response is an error
    '''
    response = test_client.get('/tupperware')
    assert response.status_code == 404