
import pytest
from application import app
from application.blueprints.users.users import users_bp

@pytest.fixture(scope="module")
def client():
    # Create a test client using the Flask application configured for testing
    app.config['TESTING'] = True
    #add the user blueprint
    app.register_blueprint(users_bp)

    client = app.test_client()
    # this is where the test runs
    yield client

def test_get_all_users(client):
    '''
    GIVEN the GET /users route is defined
    WHEN the '/users' page is requested (GET)
    THEN check that the response is valid
    '''
    response = client.get('/users')
    assert response.status_code == 200
    


