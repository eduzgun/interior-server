import pytest
from application import create_app


# Create a test client fixture
@pytest.fixture(scope='module')
def test_client():
    #define another app instance which is used for testing
    app = create_app()  
    #set the specific testing configurations found in config.py
    app.config.from_object('config.TestingConfig')
    with app.test_client() as testing_client:
        # Establish an application context
        yield testing_client


@pytest.fixture(scope='function')
def log_in_default_user(test_client):
    #login to access @login_required routes
    response = test_client.post('/auth/login', json={'username': 'grass', 'password': '123'})
    assert response.status_code == 204  

