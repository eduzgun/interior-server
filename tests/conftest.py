import os
import pytest
from application import create_app, db
from application.blueprints.rooms.model import Rooms
from application.blueprints.users.model import Users

# Create an app fixture for testing
# @pytest.fixture(scope='module')
# def app():
#     app = create_app()

#     with app.app_context():
#         yield app

# Create a test client fixture
@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'

    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


# Create a database fixture
# @pytest.fixture(scope='module')
# def init_database(test_client):
#     # Create the database and the database table
#     db.create_all()
#     # Insert user data
#     # --------------can't add user for now--------- delete this comment when POST working
#     #default_user = Users(username='orange', email="orange-email", password="123")
#     #db.session.add(default_user)
#     # Commit the changes for the users
#     db.session.commit()
#     # Insert book data
#     room = Rooms(name="Test Room", dimensions="10x10", description="A test room", theme="Test Theme", user_id=1)
#     db.session.add(room)
#     # Commit the changes for the books
#     db.session.commit()
#     yield
#     db.drop_all()

#     yield

@pytest.fixture(scope='function')
def log_in_default_user(test_client):
    test_client.post('/auth/login',
        json={'username': 'orange', 'email': 'orange-email', 'password': '123'})
        #json={'username': 'user1', 'password': 'ZXKCASASFAFA', 'email': '1@gmail.com'})

    with test_client.session_transaction() as session:
            user = Users.query.filter_by(username='orange').first()
            session['user_id'] = user.id

    yield user # this is where the testing happens!

    test_client.get('/auth/logout')


# @pytest.fixture(scope='module')
# def cli_test_client():
#     # Set the Testing configuration prior to creating the Flask application
#     os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
#     flask_app = create_app()

#     runner = flask_app.test_cli_runner()

#     yield runner  # this is where the testing happens!
