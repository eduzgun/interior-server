import json

# Assuming you have a test client and fixtures set up

def test_create_like(test_client):
    '''
    GIVEN the POST /likes route is defined
    WHEN a like is created
    THEN check that the response status code is 201
    '''
    user_id = 1
    room_id = 1

    response = test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})
    assert response.status_code == 201

def test_create_duplicate_like(test_client):
    '''
    GIVEN the POST /likes route is defined
    WHEN a duplicate like is created
    THEN check that the response status code is 400
    '''
    user_id = 1
    room_id = 1

    # Create a like
    test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})

    # Try to create a duplicate like
    response = test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})
    assert response.status_code == 400

def test_get_likes(test_client):
    '''
    GIVEN the GET /likes route is defined
    WHEN the likes are requested
    THEN check that the response is valid and contains "likes"
    '''
    response = test_client.get('/likes')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert "likes" in data

def test_get_likes_by_user(test_client):
    '''
    GIVEN the GET /likes/user/<id> route is defined
    WHEN the likes for a specific user are requested
    THEN check that the response status code is 200 and contains "data"
    '''
    user_id = 1
    response = test_client.get(f'/likes/user/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert "data" in data

def test_get_likes_by_room(test_client):
    '''
    GIVEN the GET /likes/room/<id> route is defined
    WHEN the likes for a specific room are requested
    THEN check that the response status code is 200 and contains "data"
    '''
    room_id = 1
    response = test_client.get(f'/likes/room/{room_id}')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert "data" in data

def test_delete_like(test_client):
    '''
    GIVEN the DELETE /likes/<user_id>/<room_id> route is defined
    WHEN a like is created and then deleted
    THEN check that the response status code is 204
    '''
    user_id = 1
    room_id = 1

    # Create a like
    test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})

    # Delete the like
    response = test_client.delete(f'/likes/{user_id}/{room_id}')
    assert response.status_code == 204



# Assuming you have a test client and fixtures set up

def test_create_duplicate_like(test_client):
    '''
    GIVEN the POST /likes route is defined
    WHEN a duplicate like is created
    THEN check that the response status code is 400
    '''
    user_id = 1
    room_id = 1

    # Create a like
    test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})

    # Try to create a duplicate like
    response = test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})
    assert response.status_code == 400
    assert "error" in response.json
    assert "This user already liked this room" in response.json["error"]

def test_create_like_with_internal_error(test_client, monkeypatch):
    '''
    GIVEN the POST /likes route is defined
    WHEN an internal error occurs during like creation
    THEN check that the response status code is 500
    '''
    def mock_commit_error():
        raise Exception("Simulated internal error")

    monkeypatch.setattr("application.blueprints.likes.likes.db.session.commit", mock_commit_error)

    user_id = 1
    room_id = 1

    response = test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})
    assert response.status_code == 500
    assert "error" in response.json
    assert "Something went wrong" in response.json["error"]
