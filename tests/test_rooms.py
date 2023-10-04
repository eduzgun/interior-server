
from application.blueprints.rooms.model import Rooms
from application import db

# Test case to check if all rooms can be retrieved
def test_get_all_rooms(test_client):
    '''
    GIVEN the GET /rooms route is defined
    WHEN the '/rooms' page is requested (GET)
    THEN check that the response is valid
    '''
    response = test_client.get('/rooms')
    assert response.status_code == 200



# Test case to check if a specific room can be retrieved by ID
def test_get_room_by_id(test_client):
    '''
    GIVEN the GET /rooms/{id} route is defined
    WHEN the '/rooms' page is requested (GET)
    THEN check that the response is valid
    '''

    response = test_client.get(f'/rooms/{1}')
    assert response.status_code == 200
    assert "data" in response.json
    assert "id" in response.json["data"]


# Test case to check if updating a room's details is successful
def test_update_room(test_client):
    # Add a test room to the database for this test
    room = Rooms(name="Test Room", dimensions="10x10", description="A test room", theme="Test Theme", category="Test Category", user_id=1)
    db.session.add(room)
    db.session.commit()

    update_data = {
        "name": "Updated Room Name",
        "dimensions": "Updated Dimensions",
        "description": "Updated Description",
        "theme": "Updated Theme",
        "category": "Updated Category"  # Include the 'category' field in the update
    }
    response = test_client.patch(f'/rooms/{room.id}', json=update_data)
    assert response.status_code == 200
    assert "data" in response.json
    assert response.json["data"]["name"] == "Updated Room Name"

# Test case to check if deleting a room is successful
def test_delete_room(test_client):
    # Add a test room to the database for this test
    room = Rooms(name="Test Room", dimensions="10x10", description="A test room", theme="Test Theme", user_id=1)
    db.session.add(room)
    db.session.commit()

    response = test_client.delete(f'/rooms/{room.id}')
    assert response.status_code == 204

# Test case to check if creating a room with missing data results in a BadRequest error
def test_create_room_with_missing_data(test_client):
    data = {
        "name": "Test Room",
        "dimensions": "10x10",
        "description": "A test room",
        "theme": "Test Theme",
        # Include the missing 'category' field
        "user_id": 1
    }
    response = test_client.post('/rooms', json=data)
    assert response.status_code == 201
    assert "data" in response.json


# Test case to check if retrieving a non-existent room by ID results in a NotFound error
def test_get_nonexistent_room(test_client):
    response = test_client.get('/rooms/999')
    assert response.status_code == 404
    assert "error" in response.json

