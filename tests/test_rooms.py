

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

'''
# Test case to check if updating a room's details is successful
def test_update_room(client):
    # Add a test room to the database for this test
    room = Rooms(name="Test Room", dimensions="10x10", description="A test room", theme="Test Theme", user_id=1)
    db.session.add(room)
    db.session.commit()

    update_data = {"name": "Updated Room Name"}
    response = client.patch(f'/rooms/{room.id}', json=update_data)
    assert response.status_code == 200
    assert "data" in response.json
    assert response.json["data"]["name"] == "Updated Room Name"

# Test case to check if deleting a room is successful
def test_delete_room(client):
    # Add a test room to the database for this test
    room = Rooms(name="Test Room", dimensions="10x10", description="A test room", theme="Test Theme", user_id=1)
    db.session.add(room)
    db.session.commit()

    response = client.delete(f'/rooms/{room.id}')
    assert response.status_code == 204

# Test case to check if creating a room with missing data results in a BadRequest error
def test_create_room_with_missing_data(test_client):
    data = {
        "name": "Test Room",
        "description": "A test room",
        "user_id": 1
    }
    response = client.post('/rooms', json=data)
    assert response.status_code == 400
    assert "error" in response.json

# Test case to check if retrieving a non-existent room by ID results in a NotFound error
def test_get_nonexistent_room(test_client):
    response = client.get('/rooms/999')
    assert response.status_code == 404
    assert "error" in response.json

'''

